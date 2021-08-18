import rectangle_generator
import nearest_neighbor
import rtree_generator
import query_points_generator
import NNSequentialSearch
import RangeQueryGenerator
import RangeQueries
import RangeSeqSearch

nr=10000
rectangle_generator.generate_rectangles(nr)
print("Generating R tree...")
rtree_generator.build_rtree(nr)
print("Generating query points...")
query_points_generator.gen_query_points()
print("Resolving R tree queries...")
nearest_neighbor.nearest_neighbor(nr)
print("Generating range queries...")
RangeQueryGenerator.generate_queries2(nr)
print("Resolving range queries using R tree...")
RangeQueries.range_queries(nr)
# print("Resolving range queries using sequential search...")
# RangeSeqSearch.range_search(nr)