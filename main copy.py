import itertools
from os.path import join
from data_prep import *
from matplotlib import pyplot as plt
import networkx as nx
import multiprocessing as mp
from multiprocessing.shared_memory import SharedMemory
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time



def pair_multiplexity(shape, a_layer,b_layer,start,stop):
	shared = SharedMemory(name='macierz')
	matrix = np.ndarray(shape=shape, dtype=np.int16, buffer=shared.buf)

	out = 0
	for i in range(start,stop):
		a = 1 if 1 in matrix[a_layer,i] else 0
		b = 1 if 1 in matrix[b_layer,i] else 0
		out += (a*b)

	shared.close()

	return out




if __name__ == '__main__':
	start = time.time()
    

	# wybór danych

	# dir = join('dane','CS-Aarhus_Multiplex_Social','Dataset')
	# edge_file = 'CS-Aarhus_multiplex.edges'
	# layer_file = 'CS-Aarhus_layers.txt'
	# nodes_name = 'CS-Aarhus_nodes.txt'
	
	dir = join('dane','EUAir_Multiplex_Transport','Dataset')
	edge_file = 'EUAirTransportation_multiplex.edges'
	layer_file = 'EUAirTransportation_layers.txt'
	nodes_name = 'EUAirTransportation_nodes.txt'

	# dir = join('dane','HumanMicrobiome_Multiplex_Biological','Dataset')
	# edge_file = 'HumanMicrobiome_multiplex.edges'
	# layer_file = 'HumanMicrobiome_layers.txt'
	# nodes_name = 'HumanMicrobiome_nodes.txt'



	# załadowanie danych
	edges = edge_loader(join(dir, edge_file))
	layers = layer_loader(join(dir,layer_file))
	nodes = node_loader(join(dir,nodes_name))

	# pozyskanie wielopoziomowej macierzy sąsiedztwa
	arr = edges_to_array(edges, len(layers), len(nodes))


	# dzielona pamięć
	shm = SharedMemory(name='macierz' ,create=True,size=arr.nbytes)

	arrShar = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf)
	arrShar[:] = arr[:]





	N = mp.cpu_count()
	M = len(nodes)
	stops = [i*(M//N) for i in range(N)]
	stops[-1] = M

	


	# dla każdej pary poziomów w sieci oblicz pairwise multiplexity i ustaw jako wagę krawędzi
	G = nx.Graph()
	with ProcessPoolExecutor(N) as pool:
		for i,j in itertools.combinations(range(len(layers)), 2):
			results = pool.map(pair_multiplexity,
				itertools.repeat(arr.shape,len(stops)-1),
				itertools.repeat(i,len(stops)-1),
				itertools.repeat(j,len(stops)-1),
				stops[:-1],
				stops[1:])

			weight = sum([result for result in results]) / M

			G.add_edge(i,j, weight = weight)


	shm.close()
	shm.unlink()
 
	# przeskalowanie wag na grubości krawędzi
	weights = list( nx.get_edge_attributes(G, 'weight').values() )
	scaled = [w*10 for w in weights]
	
	pos = nx.circular_layout(G)
	# pos = nx.spring_layout(G)
	# pos = nx.kamada_kawai_layout(G)

	nx.draw_networkx_nodes(G, pos)
	nx.draw_networkx_labels(G,pos,layers, bbox=dict(facecolor='yellow', alpha=.25))#, font_weight='bold'
	nx.draw_networkx_edges(G,pos, width=scaled, edge_color='#707070')	#, connectionstyle='Angle, angleA=90, angleB=20, rad=0.2'  , edge_color='#4169e1'
 
	finish = time.time()
	print(f'Czas wykonania: {finish-start}')
