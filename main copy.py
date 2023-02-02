import itertools
from os.path import join
from data_prep import edge_loader, layer_loader, node_loader, edges_to_array
from matplotlib import pyplot as plt
import networkx as nx
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import copy
import asyncio




def main():
	start = time.time()
    

	# wybór danych

	dir = join('dane','CS-Aarhus_Multiplex_Social','Dataset')
	edge_file = 'CS-Aarhus_multiplex.edges'
	layer_file = 'CS-Aarhus_layers.txt'
	nodes_name = 'CS-Aarhus_nodes.txt'
	
	# dir = join('dane','EUAir_Multiplex_Transport','Dataset')
	# edge_file = 'EUAirTransportation_multiplex.edges'
	# layer_file = 'EUAirTransportation_layers.txt'
	# nodes_name = 'EUAirTransportation_nodes.txt'

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

	# Przygotowanie egzekutora
	N = mp.cpu_count()
	pool = ThreadPoolExecutor(N)
	# pool = ProcessPoolExecutor(N)

	# przygotowanie zakresów dla wątków/procesów
	M = len(nodes)
	stops = [i*(M//N) for i in range(N)]
	stops[-1] = M

	# dla każdej pary poziomów w sieci oblicz pairwise multiplexity i ustaw jako wagę krawędzi
	cor_edges = [[i,j] for i,j in itertools.combinations(range(len(layers)), 2)]
	G = nx.Graph()
	# with ProcessPoolExecutor(N) as pool:
	for i,j in cor_edges:
		futures = [pool.submit(pair_multiplexity, arr, i, j, stops[k], stops[k+1])			for k in range(len(stops) - 1)]
		weight = sum([future.result() for future in futures]) / M

		G.add_edge(i,j, weight = weight)

	# przeskalowanie wag na grubości krawędzi
	weights = list( nx.get_edge_attributes(G, 'weight').values() )
	scaled = [w*10 for w in weights]
	
	# pos = nx.circular_layout(G)
	pos = nx.spring_layout(G)
	# pos = nx.kamada_kawai_layout(G)

	nx.draw_networkx_nodes(G, pos)
	nx.draw_networkx_labels(G,pos,layers, bbox=dict(facecolor='yellow', alpha=.25))#, font_weight='bold'
	nx.draw_networkx_edges(G,pos, width=scaled, edge_color='#4169e1')	#, connectionstyle='Angle, angleA=90, angleB=20, rad=0.2'

	finish = time.time()
	print(f'Czas wykonania: {finish-start}')

	plt.show()








def pair_multiplexity(matrix, a_layer, b_layer, start, stop):
	out = 0
	for i in range(start,stop):
		a = 1 if 1 in matrix[a_layer,i] else 0
		b = 1 if 1 in matrix[b_layer,i] else 0
		out += (a*b)

	return out


async def test(matrix):
	out = 0
	for i in range(100):
		out+=1

	return out/100




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



	N = mp.cpu_count()
	M = len(nodes)
	stops = [i*(M//N) for i in range(N)]
	stops[-1] = M

	
	

	# dla każdej pary poziomów w sieci oblicz pairwise multiplexity i ustaw jako wagę krawędzi
	G = nx.Graph()
	# with ProcessPoolExecutor(N) as pool:
	# 	for i,j in itertools.combinations(range(len(layers)), 2):
	# 		results = pool.map(test)

	# 		weight = sum([result for result in results]) / M

	# 		G.add_edge(i,j, weight = weight)


	with mp.Pool(N) as pool:
		for i,j in itertools.combinations(range(len(layers)), 2):
			# pool.submit(pair_multiplexity, arr, i, j, stops[k], stops[k+1])			for k in range(len(stops) - 1)
			processes = [pool.apply_async(test,(arr,)) for k in range(len(stops) - 1)]
			results = [process.get() for process in processes]
	# 		weight = sum([result for result in results]) / M

	# 		G.add_edge(i,j, weight = weight)


	finish = time.time()
	print(f'Czas wykonania: {finish-start}')