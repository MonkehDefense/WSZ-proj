import itertools
import numpy as np
from os.path import join
from data_prep import edge_loader, layer_loader, node_loader, edges_to_array

def main():
	dir = join('dane','CS-Aarhus_Multiplex_Social','Dataset')
	edge_file = 'CS-Aarhus_multiplex.edges'
	layer_file = 'CS-Aarhus_layers.txt'
	nodes_name = 'CS-Aarhus_nodes.txt'

	edges = edge_loader(join(dir, edge_file))
	layers = layer_loader(join(dir,layer_file))
	nodes = node_loader(join(dir,nodes_name))

	# for edge in edges:
	# 	print(edge)
	# print(layers)
	# print(len(nodes))

	arr = edges_to_array(edges, len(layers), len(nodes))

	cor_edges = [(i,j) for i,j in itertools.combinations(range(len(layers)), 2)]
	cor_weights = []
	for i,j in cor_edges:
		cor_weights.append(pair_multiplexity(arr, i, j, len(nodes)))



def pair_multiplexity(matrix, a_layer, b_layer, N):
	out = 0
	for i in range(N):
		a = 1 if 1 in matrix[a_layer,i] else 0
		b = 1 if 1 in matrix[b_layer,i] else 0
		out += (a*b)

	return out/N

def Hamming_dist(matrix, a_layer, b_layer, N):
	out = 0
	N_a = 0
	N_b = 0
	for i in range(N):
		a = 1 if 1 in matrix[a_layer,i] else 0
		b = 1 if 1 in matrix[b_layer,i] else 0
		N_a += a
		N_b += b
		out += (b*(1-b) + a*(1-a))

	divide = min(N_a + N_b, N)

	return out/divide


def cond_prob(matrix, a_layer, b_layer, k_a, k_b, N):
	sum_a = 0
	sum_b = 0
	for i in range(N):
		check = True if np.sum(matrix[a_layer, i]) == k_a else False
		if check:
			sum_a+=1
			check = True if np.sum(matrix[b_layer, i]) == k_b else False
			sum_b = sum_b + 1 if check else sum_b

	if sum_a != 0:
		return sum_b/sum_a

	return 0


def inter_layer_cor(matrix, a_layer, b_layer, k_a, N):
	k_set = set()
	k_set.update([np.sum(matrix[b_layer,i]) for i in range(N)])

	out = 0
	for k in k_set:
		out += (k * cond_prob(matrix, a_layer, b_layer, k_a, k, N))
	return out




if __name__ == '__main__':
	main()