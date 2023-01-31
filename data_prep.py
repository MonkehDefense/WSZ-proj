from os.path import join
#from os import listdir
import numpy as np

#https://manliodedomenico.com/data.php

def main():
	dir = join('dane','CS-Aarhus_Multiplex_Social','Dataset')
	edge_file = 'CS-Aarhus_multiplex.edges'
	layer_file = 'CS-Aarhus_layers.txt'
	nodes_name = 'CS-Aarhus_nodes.txt'

	edges = edge_loader(join(dir, edge_file))
	layers = layer_loader(join(dir,layer_file))
	nodes = node_loader(join(dir,nodes_name))


	arr = edges_to_array(edges, len(layers), len(nodes))

	print(layers)

	# for edge in edges:
	# 	print(edge)
	# print(layers)
	# print(len(nodes))


def edge_loader(path):
	# layerID nodeID nodeID weight
	edges = []
	
	with open(path) as file:
		for line in file:
			contents = [int(i) - 1 for i in line.split(sep=' ')[:-1]]
			edges.append(contents)

	return edges

def layer_loader(path):
	layers = dict()
	
	with open(path) as file:
		i = True
		for line in file:
			if i:
				i = not i
				continue
			contents = line.split(sep=' ')
			contents[1] = contents[1].replace('\n','').replace('_',' ')

			contents[0] = int(contents[0]) - 1
			# layers.append(contents)
			layers[contents[0]] = contents[1]
	return layers

def node_loader(path):
	nodes = []
	
	with open(path) as file:
		i = True
		for line in file:
			if i:
				i = not i
				continue
			contents = line.split(sep=' ')
			contents[0] = int(contents[0]) - 1
			nodes.append(contents)
	return nodes


def edges_to_array(edges, layers, nodes):
	arr = np.zeros((layers, nodes, nodes))
	
	for i in range(len(edges)):
		edge = edges[i]

		arr[edge[0],edge[1],edge[2]] = 1
		arr[edge[0],edge[2],edge[1]] = 1

	return arr

if __name__ == '__main__':
	main()