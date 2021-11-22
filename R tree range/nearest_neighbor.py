from rtree_node import node
import json
import pickle5 as pickle
import math
import sys
import time

max_size = sys.maxsize
dict1=dict()
class BranchListElement:
    """Class to represent an element of the active branch list"""
    def __init__(self, rectangle, id, point, dimen):
        self.rectangle_id = id
        self.mindist = calcMinDist(point, rectangle, dimen)
        self.minmaxdist = calcMinMaxDist(point, rectangle, dimen)
    
def calcMinDist(point, rectangle, dimen):
    mindist = 0
    for i in range(0,dimen):
        r=point[i]
        if point[i]<rectangle[i][0]:
            r = rectangle[i][0]
        elif point[i]>rectangle[i][1]:
            r = rectangle[i][1]
        mindist += math.pow(point[i]-r,2)
    return mindist

def calcMinMaxDist(point, rectangle, dimen):
    minmaxdist=max_size
    for k in range(0,dimen):
        rm = rectangle[k][1]
        if point[k]<=(rectangle[k][0]+rectangle[k][1])/2:
            rm = rectangle[k][0]
        sum = math.pow(point[k]-rm,2)
        for i in range(0,dimen):
            if i==k:
                continue
            rM = rectangle[i][1]
            if point[i]>=(rectangle[i][0]+rectangle[i][1])/2:
                rM = rectangle[i][0]
            sum += math.pow(point[i]-rM,2)
        minmaxdist = min(minmaxdist,sum)
    return minmaxdist

def genBranchList(bounding_rectangles, point, dimen):
    abl = []
    i = 0
    for rec in bounding_rectangles:
        elem = BranchListElement(rec, i, point)
        i += 1
        abl.append(elem)
    return abl

def downwardPruning(abl, nearestDist):
    mindistThreshold = nearestDist
    for i in range(0, len(abl)):
        if mindistThreshold < abl[i].mindist:
            return i
        if abl[i].minmaxdist < mindistThreshold:
            mindistThreshold = abl[i].minmaxdist
    return i

def nearestNeighborSearch(node, point, nearestDist, nearestNeighbor, nodesVisited, dimen):
    nodesVisited += 1
    if node.isLeaf == True:
        for rec in node.bounding_rectangles:
            dist = calcMinDist(point, rec, dimen)
            if dist<nearestDist:
                nearestDist = dist
                nearestNeighbor = rec
        return nearestDist, nearestNeighbor, nodesVisited
    # abl = genBranchList(node.bounding_rectangles, point)
    abl = []
    i = 0
    for rec in node.bounding_rectangles:
        elem = BranchListElement(rec, i, point, dimen)
        i += 1
        abl.append(elem)
    abl = sorted(abl, key = lambda x: x.mindist)

    for i in range(0, len(abl)):
        if nearestDist <= abl[i].mindist:
            break
        if abl[i].minmaxdist < nearestDist:
            nearestDist = abl[i].minmaxdist
    last = i
    # last = downwardPruning(abl, nearestDist)
    for i in range(0,last+1):
        if abl[i].mindist>=nearestDist:
            break
        newnode = node.children_[abl[i].rectangle_id]
        nearestDist, nearestNeighbor, nodesVisited = nearestNeighborSearch(newnode, point, nearestDist, nearestNeighbor, nodesVisited, dimen)
        
    return nearestDist, nearestNeighbor, nodesVisited
    
def nearest_neighbor(nr):
    queryfile = open("nnqueries.txt","r")
    queries = json.load(queryfile)
    rtreefile = open("rtree.pkl","rb")
    root = pickle.load(rtreefile)
    dimen = len(root.bounding_rectangles[0])
    outfilename = str(nr)+"rectanglesNNSearchOutput.txt"
    outputFile = open(outfilename,"w")
    # resultsFile = open("NNSearchResults.txt","a")
    res=[]
    totalTime = 0
    totalNodes = 0
    for point in queries:
        nearestDist = max_size
        nearestNeighbor = []
        nodesVisited = 0
        start = time.time()
        nearestDist, nearestNeighbor, nodesVisited = nearestNeighborSearch(root, point, nearestDist, nearestNeighbor, nodesVisited, dimen)
        end = time.time()
        timeInterval = end-start
        totalTime += timeInterval
        totalNodes += nodesVisited
        res.append([timeInterval, nearestDist, nearestNeighbor, nodesVisited])

    json.dump(res, outputFile)
    n = len(queries)
    avgTime = totalTime/n
    avgNodesVisited = totalNodes/n
    # resultsFile.write(str(nr)+" rectangles: ")
    # resultsFile.write(str(avgTime)+' '+str(avgNodesVisited) + '\n')
    print(avgNodesVisited)

    