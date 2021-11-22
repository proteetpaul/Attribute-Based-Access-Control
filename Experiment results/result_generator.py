import data_generator_new
import skewed_request_generator
import abac_system_to_rectangle_converter
import query_converter_abac
import rtree_generator
import poltree_generator
import poltree_resolve
import rtree_search_abac
import query_checker
import bin_poltree_generate
import bin_poltree_resolve
import Rtree_depth
import sys

# sys.setrecursionlimit(10000)
np = 10000
# np = int(input("Enter no. of policies:\n"))
# print("Policies = "+str(np))
# data_generator_new.generate_data(np)
# print("Generating random access requests...")
# skewed_request_generator.gen_requests(500)
# print("Converting policies to rectangles...")
# abac_system_to_rectangle_converter.convert_rectangles()
# print("converting queries to rectangles...")
# query_converter_abac.query_converter_abac()
# print("Generating R tree...")
# rtree_generator.build_rtree()
# print("Resolving R tree requests...")
# rtree_search_abac.resolve_queries(np)
# print("Building n-ary poltree...")
# poltree_generator.generator()
# print("Resolving poltree requests...")
# poltree_resolve.resolve(np)
# print("Resolving sequential search requests...")
# query_checker.resolve(np)
# Rtree_depth.get_depth()
# print("Generating binary poltree...")
# bin_poltree_generate.generator()
print("Resolving binary poltree queries...")
bin_poltree_resolve.resolve(np)


