import rectangle_generator
import nearest_neighbor
import rtree_generator
import query_points_generator
import NNSequentialSearch

rectangle_generator.generate_rectangles()
print("Generating R tree...")
rtree_generator.build_rtree()
print("Generating query points...")
query_points_generator.gen_query_points()
print("Resolving R tree queries...")
nearest_neighbor.nearest_neighbor()
print("Resolving sequential search queries...")
NNSequentialSearch.seq_search_nn()