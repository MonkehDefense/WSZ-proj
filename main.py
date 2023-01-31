import itertools
import numpy as np
from os.path import join
from data_prep import edge_loader, layer_loader, node_loader, edges_to_array
from matplotlib import pyplot as plt
import networkx as nx
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor




def main():
	dir = join('dane','CS-Aarhus_Multiplex_Social','Dataset')
	edge_file = 'CS-Aarhus_multiplex.edges'
	layer_file = 'CS-Aarhus_layers.txt'
	nodes_name = 'CS-Aarhus_nodes.txt'

	
	# dir = join('dane','EUAir_Multiplex_Transport','Dataset')
	# edge_file = 'EUAirTransportation_multiplex.edges'
	# layer_file = 'EUAirTransportation_layers.txt'
	# nodes_name = 'EUAirTransportation_nodes.txt'

	
	# dir = join('dane','London_Multiplex_Transport','Dataset')
	# edge_file = 'london_transport_multiplex.edges'
	# layer_file = 'london_transport_layers.txt'
	# nodes_name = 'london_transport_nodes.txt'

	edges = edge_loader(join(dir, edge_file))
	layers = layer_loader(join(dir,layer_file))
	nodes = node_loader(join(dir,nodes_name))

	arr = edges_to_array(edges, len(layers), len(nodes))

	cor_edges = [[i,j] for i,j in itertools.combinations(range(len(layers)), 2)]
	weights = []
	G = nx.Graph()

	for i,j in cor_edges:
		G.add_edge(i,j, weight = pair_multiplexity(arr, i, j, len(nodes)))

	weights = list( nx.get_edge_attributes(G, 'weight').values() )
	scaled = [w*4 for w in weights]
	

	pos = nx.circular_layout(G)
	nx.draw(G, pos, with_labels = True, font_weight = 'bold', width = scaled, labels = layers)
	plt.show()








def pair_multiplexity(matrix, a_layer, b_layer, N):
	out = 0
	for i in range(N):
		a = 1 if 1 in matrix[a_layer,i] else 0
		b = 1 if 1 in matrix[b_layer,i] else 0
		out += (a*b)

	return out/N




# public static BufferedImage gen_pic(int w, int h, double cr_left, double cr_right, double ci_top, double ci_bottom, int iter, int[] chunkSize, ThreadPoolExecutor exec) throws InterruptedException {
	# double cr_span, ci_span;
	# cr_span = cr_right - cr_left;
	# ci_span = ci_top - ci_bottom;
	# BufferedImage img = new BufferedImage(w,h,BufferedImage.TYPE_INT_RGB);


	# CountDownLatch cl = new CountDownLatch((w/chunkSize[0]) * (h/chunkSize[1]));

	# for(int i = 0; i < w; i+=chunkSize[0]){
		# for(int j = 0; j < h; j+=chunkSize[1]){
			# final int start_x = i, stop_x, start_y = j, stop_y;

			# if(start_x + 2 * chunkSize[0] > w){
				# stop_x = w;
			# } else{stop_x = start_x + chunkSize[0];}

			# if(start_y + 2 * chunkSize[1] > h){
				# stop_y = h;
			# } else{stop_y = start_y + chunkSize[1];}

			# exec.execute(() -> {
				# for(int x = start_x; x < stop_x; x++){
					# for(int y = start_y; y < stop_y; y++){
						# double zi = 0, zr = 0, z_abs = 0, cr, ci;

						# // konwersja pikseli na ci i cr
						# ci = ci_top - y * ci_span / h;
						# cr = x * cr_span / w + cr_left;

						# int itr = 0;
						# while(itr < iter && z_abs < 2){
							# double zrzr = zr*zr;
							# double zizi = zi*zi;

							# zi = 2.0 * zr * zi + ci;
							# zr = zrzr - zizi + cr;
							# z_abs = Math.sqrt(zizi + zrzr);
							
							# itr++;
						# }
						
							
							
						# if(itr == iter){
						#    img.setRGB(x, y, new Color(100,0,0).getRGB());
						# } else {
							# int clr_aux = 255 - (int)Math.floor(255.0 * (double)itr/(double)iter);
							# img.setRGB(x, y, new Color(clr_aux,255,clr_aux).getRGB());
						# }


					# }
				# }

				# cl.countDown();
			# });

		# }
	# }
	   

	# cl.await();

	# return img;
# }



if __name__ == '__main__':
	main()