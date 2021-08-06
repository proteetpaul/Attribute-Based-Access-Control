from rtree_node import node
import json
import pickle5 as pickle
import math
import sys
import time

dimen = 0
class BranchListElement:
    """Class to represent an element of the active branch list"""
    def __init__(self, rectangle, id, point):
        self.rectangle_id = id
        self.mindist = calcMinDist(point, rectangle)
        self.minmaxdist = calcMinMaxDist(point, rectangle)
    
def calcMinDist(point, rectangle):
    global dimen
    mindist = 0
    for i in range(0,dimen):
        r=point[i]
        if point[i]<rectangle[i][0]:
            r = rectangle[i][0]
        elif point[i]>rectangle[i][1]:
            r = rectangle[i][1]
        mindist += math.pow(point[i]-r,2)
    return mindist

def calcMinMaxDist(point, rectangle):
    minmaxdist=sys.maxsize
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

def genBranchList(bounding_rectangles, point):
    global dimen
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

def nearestNeighborSearch(node, point, nearestDist, nearestNeighbor):
    global dimen
    if node.isLeaf == True:
        for rec in node.bounding_rectangles:
            dist = calcMinDist(point, rec)
            if dist<nearestDist:
                nearestDist = dist
                nearestNeighbor = rec
        return nearestDist, nearestNeighbor
    # abl = genBranchList(node.bounding_rectangles, point)
    abl = []
    i = 0
    for rec in node.bounding_rectangles:
        elem = BranchListElement(rec, i, point)
        i += 1
        abl.append(elem)
    sorted(abl, key = lambda x: x.mindist)

    mindistThreshold = nearestDist
    for i in range(0, len(abl)):
        if mindistThreshold < abl[i].mindist:
            break
        if abl[i].minmaxdist < mindistThreshold:
            mindistThreshold = abl[i].minmaxdist
    last = i
    # last = downwardPruning(abl, nearestDist)
    for i in range(0,last+1):
        if abl[i].mindist>=nearestDist:
            break
        newnode = node.children_[abl[i].rectangle_id]
        nearestDist, nearestNeighbor = nearestNeighborSearch(newnode, point, nearestDist, nearestNeighbor)
        
    return nearestDist, nearestNeighbor
    
def nearest_neighbor():
    global dimen
    queryfile = open("nnqueries.txt","r")
    queries = json.load(queryfile)
    rtreefile = open("rtree.pkl","rb")
    root = pickle.load(rtreefile)
    dimen = len(root.bounding_rectangles[0])
    outputFile = open("NNSearchOutput.txt","w")
    resultsFile = open("NNSearchResults.txt","a")
    res=[]
    totalTime = 0
    for point in queries:
        nearestDist = sys.maxsize
        nearestNeighbor = []
        start = time.time()
        nearestDist, nearestNeighbor = nearestNeighborSearch(root, point, nearestDist, nearestNeighbor)
        end = time.time()
        timeInterval = end-start
        totalTime += timeInterval
        res.append([timeInterval, nearestDist, nearestNeighbor])
    json.dump(res, outputFile)
    n = len(queries)
    avgTime = totalTime/n
    resultsFile.write('\n'+str(avgTime))

    