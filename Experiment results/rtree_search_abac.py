import json
import time
import pickle
from rtree_node import node
import sys
from anytree import RenderTree


def CheckOverlap(rec1, rec2, dimen):
    """ Check overlap between 2 rectangles """
    for i in range(0, dimen):
        if rec1[i][1] < rec2[i][0] or rec1[i][0] > rec2[i][1]:
            return False
    return True

def CalcDepth(root):
    if root.isLeaf==0:
        return 1
    return 1+CalcDepth(root.children_[0])

def SearchTreeForOverlap(n, rectangle, dimen, nodesVisited):
    nodesVisited=nodesVisited+1
    """ Search the tree to find overlapping rectangles """
    for i in range(0, len(n.bounding_rectangles)):
        overlap = True#CheckOverlap(n.bounding_rectangles[i], rectangle)
        rec2 = n.bounding_rectangles[i]
        for j in range(0, dimen):
            if rectangle[j][1] < rec2[j][0] or rectangle[j][0] > rec2[j][1]:
                overlap = False
                break
    
        if overlap == True:
            if n.isLeaf==1:
                return 1, nodesVisited
            else:
                leafFound, nodesVisited = SearchTreeForOverlap(n.children_[i], rectangle, dimen, nodesVisited)
                if leafFound == 1:
                    return 1, nodesVisited
    return 0, nodesVisited

def resolve_queries(np):
    nodesVisited = 0
    inputfile = open("rtree.pkl", "rb")
    inputfile2 = open("rtreeparams.txt", "r")
    root = pickle.load(inputfile)
    dimen = int(inputfile2.readline())
    print(dimen)
    leafFound = 0
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
        start = time.time()
        decision, nodesVisited = SearchTreeForOverlap(root, rec, dimen, nodesVisited)
        end = time.time()
        times.append(end-start)
        if decision == 1:
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

    outfilename = str(np)+"policies_rtree_output.txt"
    outputfile = open(outfilename, "w")
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
    results_file.write(str(np)+' policies')
    json.dump(list1, results_file, indent=4)