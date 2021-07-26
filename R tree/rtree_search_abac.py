import json
import time
import pickle
from rtree_node import node
import sys
from anytree import RenderTree


inputfile = open("rtree.pkl", "rb")
inputfile2 = open("rtreeparams.txt", "r")
root = pickle.load(inputfile)
dimen = int(inputfile2.readline())
print(dimen)
nodesVisited = 0
leafFound = 0

def CheckOverlap(rec1, rec2):
    """ Check overlap between 2 rectangles """
    global dimen
    for i in range(0, dimen):
        if rec1[i][1] < rec2[i][0] or rec1[i][0] > rec2[i][1]:
            return False
    return True


def SearchTreeForOverlap(n, rectangle, resultList):
    global nodesVisited, leafFound
    nodesVisited=nodesVisited+1
    """ Search the tree to find overlapping rectangles """
    for i in range(0, len(n.bounding_rectangles)):
        if CheckOverlap(rectangle, n.bounding_rectangles[i]):
            if n.isLeaf==1:
                resultList.append(n.bounding_rectangles[i])
                leafFound = 1
            else:
                SearchTreeForOverlap(n.children_[i], rectangle, resultList)
            if leafFound == 1:
                return


queries_file = open("rtree_queries.txt", "r")
results_file = open("rtree_results.txt", "a")
queryRectangles = json.load(queries_file)
result = []
times = []
nallowed = 0
ndenied = 0
totalTimeAllowed = 0
totalTimeDenied = 0
nodesVisitedAllowed = 0
nodesVisitedDenied = 0
for rec in queryRectangles:
    resultList = []
    start = time.time()
    SearchTreeForOverlap(root, rec, resultList)
    end = time.time()
    times.append(end-start)
    if len(resultList) > 0:
        result.append(['Yes', nodesVisited])
        totalTimeAllowed += end-start
        nallowed += 1
        nodesVisitedAllowed += nodesVisited
    else:
        result.append('No')
        totalTimeDenied += end-start
        nodesVisitedDenied += nodesVisited
        ndenied += 1 
    nodesVisited = 0
    leafFound = 0

outputfile = open("output.txt", "w")
json.dump(result, outputfile, indent=4)
json.dump(times, outputfile, indent=4)

if nallowed>0:
    avgTimeAllowed = totalTimeAllowed/nallowed
    avgNodesVisitedAllowed = nodesVisitedAllowed/nallowed
if ndenied>0:
    avgTimeDenied = totalTimeDenied/ndenied
    avgNodesVisitedDenied = nodesVisitedDenied/ndenied
avgTime = (totalTimeAllowed + totalTimeDenied)/(nallowed + ndenied)
avgNodesVisited = (nodesVisitedAllowed + nodesVisitedDenied)/(nallowed + ndenied)
list1 = [avgTimeAllowed, avgTimeDenied, avgTime, avgNodesVisitedAllowed, avgNodesVisitedDenied, avgNodesVisited]
json.dump(list1, results_file, indent=4)