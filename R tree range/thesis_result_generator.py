import abac_request_generator
import data_generator_new
import NNSequentialSearch
import RangeQueryGenerator
import RangeQueries
import rtree_generator
import abac_to_rectangle
import RangeSeqSearch

np = 20000
data_generator_new.generate_data(np)
abac_to_rectangle.convert_rectangles(np)
rtree_generator.build_rtree(np)
abac_request_generator.generate_requests(500, np)
abac_request_generator.request_to_rectangle(np)
NNSequentialSearch.seq_search_nn(np)
RangeQueryGenerator.generate_queries2(np)
RangeQueries.range_queries(np)
# RangeSeqSearch.range_search(np)