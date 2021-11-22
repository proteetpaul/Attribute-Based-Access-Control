import pickle
import json
from cnd_tree_classes import hds_rectangle, cnd_tree_node
from range_search import range_search
import cnd_tree_generator

nr = 12
rectangles = list()
cds_lengths = [4,4]
ndds_lengths = [2, 2, 2, 2]
cdimen = 2
ddimen = 4
inputfile = open("example_policy.txt", "r")
# marketing:0, engineering: 1
# associate:0, group leader: 1
# weekday:0, weekend: 1
# doc:0, pdf: 1
for i in range(0,12):
    x=hds_rectangle()
    arr = inputfile.readline().split() #int(input("Desgination:"))
    v1 = int(arr[0])
    v2 = int(arr[1])
    v3 = int(arr[2])
    v4 = int(arr[3])
    v5 = int(arr[4])
    v6 = int(arr[5])
    x.d_arr = [{v1}, {v2}, {v3}, {v4}]
    x.c_arr = [ [v5,v5], [v6,v6] ]
    rectangles.append(x)

filename = str(nr)+"rectangles.pkl"
file = open(filename, "wb")
pickle.dump(rectangles, file)
cdsfile = open("cds_lengths.txt","w")
json.dump(cds_lengths, cdsfile)
nddsfile = open("ndds_lengths.txt", "w")
json.dump(ndds_lengths, nddsfile)
cdsfile.close()
nddsfile.close()
file.close()

cnd_tree_generator.build_rtree(12)
cndtreefile = open("cndtree.pkl","rb")
root = pickle.load(cndtreefile)
point = hds_rectangle()
point.c_arr = [[2,2],[1,1]]
point.d_arr = [{0},{0},{0},{0}]
reslist = []
nodesVisited = range_search(root, 1,reslist, point, 2,4,0)
print(nodesVisited)
print(len(reslist))