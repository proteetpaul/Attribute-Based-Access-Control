import rtree_generator
import approx_range_search
import RangeQueryGenerator
import nearest_neighbor

nr=10000
print("Generating R tree")
rtree_generator.build_rtree(nr)
# print("Resolving R tree queries...")
# nearest_neighbor.nearest_neighbor(nr)
print("Generating range queries...")
RangeQueryGenerator.generate_queries2(nr)
print("Resolving range queries using R tree...")
approx_range_search.range_queries(nr)