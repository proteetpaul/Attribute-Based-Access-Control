import pickle
import random
import json
import time
from anytree import NodeMixin, RenderTree


class node(NodeMixin):
    """ Class to represent rtree node """

    def __init__(self, id):
        super(node, self).__init__()
        self.id = id
        self.bounding_rectangles = list()
        self.children_ = list()
        self.isLeaf = True
        self.parent = None


nqueries = int(input("Enter no. of queries:"))
inputfile = open("rtree.pkl", "rb")
inputfile2 = open("rtreeparams.txt", "r")
root = pickle.load(inputfile)
for pre,_,node1 in RenderTree(root):
    print("%s%s %s" % (pre,node1.id,len(node1.bounding_rectangles)))
dimen = int(inputfile2.readline())
limits = json.load(inputfile2)
queryRectangles = []
for i in range(0, nqueries):
    rectangle = []
    for j in range(0, dimen):
        l = random.randint(limits[j][0], limits[j][1]-1)
        u = random.randint(l+1, limits[j][1])
        rectangle.append([l, u])
    queryRectangles.append(rectangle)


def CheckOverlap(rec1, rec2):
    """ Check overlap between 2 rectangles """
    global dimen
    for i in range(0, dimen):
        if rec1[i][1] <= rec2[i][0] or rec1[i][0] >= rec2[i][1]:
            return False
    return True


def SearchTreeForOverlap(n, rectangle, resultList):
    """ Search the tree to find overlapping rectangles """
    for i in range(0, len(n.bounding_rectangles)):
        if CheckOverlap(rectangle, n.bounding_rectangles[i]):
            if n.isLeaf:
                resultList.append(n.bounding_rectangles[i])
            else:
                SearchTreeForOverlap(n.children_[i], rectangle, resultList)


result = []
times=[]
for rec in queryRectangles:
    resultList = []
    start=time.time()
    SearchTreeForOverlap(root, rec, resultList)
    end=time.time()
    times.append(end-start)
    result.append(resultList)

outputfile = open("output.txt", "w")
json.dump(result, outputfile, indent=4)
json.dump(times,outputfile,indent=4)

outputfile2=open("queries.txt","w")
json.dump(queryRectangles, outputfile2, indent=4)
