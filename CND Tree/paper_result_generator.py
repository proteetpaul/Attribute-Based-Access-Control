import cnd_tree_generator
import nearest_neighbor_search
import range_query_generator
import nnqueries
import range_search
import range_search_seq
import abac_request_generator
import abac_to_rectangle
import data_generator_new
import tree_depth

nr = 1000
data_generator_new.generate_data(nr)
abac_to_rectangle.convert_rectangles(nr)
cnd_tree_generator.build_rtree(nr)
# tree_depth.get_depth()
abac_request_generator.generate_requests(500, nr)
abac_request_generator.request_to_rectangle(nr)
nearest_neighbor_search.seq_search_nn(nr)
range_query_generator.generate_queries(nr)
range_search.func(nr)
range_search_seq.seq_range_search(nr)



