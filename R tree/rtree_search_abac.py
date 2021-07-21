import json
import time
import pickle
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


inputfile = open("rtree.pkl", "rb")
inputfile2 = open("rtreeparams.txt", "r")
root = pickle.load(inputfile)
for pre, _, node1 in RenderTree(root):
    print("%s%s %s" % (pre, node1.id, len(node1.bounding_rectangles)))
inputfile2.readline()
dimen = int(inputfile2.readline())
print(dimen)

def CheckOverlap(rec1, rec2):
    """ Check overlap between 2 rectangles """
    global dimen
    for i in range(0, dimen):
        if rec1[i][1] < rec2[i][0] or rec1[i][0] > rec2[i][1]:
            return False
    return True


def SearchTreeForOverlap(n, rectangle, resultList):
    """ Search the tree to find overlapping rectangles """
    for i in range(0, len(n.bounding_rectangles)):
        if CheckOverlap(rectangle, n.bounding_rectangles[i]):
            if n.isLeaf==1:
                resultList.append(n.bounding_rectangles[i])
            else:
                SearchTreeForOverlap(n.children_[i], rectangle, resultList)


queries_file = open("rtree_queries.txt", "r")
queryRectangles = json.load(queries_file)
result = []
times = []
for rec in queryRectangles:
    resultList = []
    start = time.time()
    SearchTreeForOverlap(root, rec, resultList)
    end = time.time()
    times.append(end-start)
    if len(resultList) > 0:
        result.append('Yes')
    else:
        result.append('No')

outputfile = open("output.txt", "w")
json.dump(result, outputfile, indent=4)
json.dump(times, outputfile, indent=4)
