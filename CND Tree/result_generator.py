import cnd_tree_generator
import nearest_neighbor_search
import range_query_generator
import nnqueries
import range_search
import range_search_seq
import rectangle_generator

nr = 1000
cdimen = 5
ddimen = cdimen
rectangle_generator.generate_rectangles(nr, cdimen, ddimen)
cnd_tree_generator.build_rtree(nr)
nnqueries.generate_queries(nr, cdimen, ddimen)
nearest_neighbor_search.seq_search_nn(nr)
range_query_generator.generate_queries(nr)
range_search.func(nr)
range_search_seq.seq_range_search(nr)
