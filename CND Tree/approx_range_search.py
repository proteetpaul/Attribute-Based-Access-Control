import json
import time
import sys
import math
import pickle
from cnd_tree_classes import *
from nearest_neighbor_search import calcDist

def approx_range_search(node, dist, reslist, point, cdimen, ddimen, nodesVisited,a):
    k = 1 + a*node.height 
    nodesVisited += 1
    n = len(node.dmbrs)
    if node.isLeaf == True:
        for i in range(0,n):
            rec = hds_rectangle()
            if cdimen > 0:
                rec.c_arr = node.cmbrs[i]
            rec.d_arr = node.dmbrs[i]
            if dist >= calcDist(point, rec, cdimen, ddimen) * k:
                reslist.append(rec)
        return nodesVisited
    for i in range(0,n):
        rec = hds_rectangle()
        if cdimen > 0:
            rec.c_arr = node.cmbrs[i]
        rec.d_arr = node.dmbrs[i]
        if dist >= calcDist(point, rec, cdimen, ddimen) * k:
            nodesVisited = approx_range_search(node.children_[i], dist, reslist, point, cdimen, ddimen, nodesVisited,a)
    return nodesVisited

def func(nr, k):
    recfilename = str(nr)+"rectangles.pkl"
    recfile = open(recfilename,"rb")
    reclist = pickle.load(recfile)
    cndtreefile = open("cndtree.pkl","rb")
    root = pickle.load(cndtreefile)
    outfilename = str(k)+str(nr)+"rectangles_rangeoutput.txt"
    outfile = open(outfilename, "w")
    nnqueryfile = open(str(nr)+"nnqueries.pkl","rb")
    points = pickle.load(nnqueryfile)
    cdimen = 0
    if len(root.cmbrs) > 0:
        cdimen = len(root.cmbrs[0])
    ddimen = len(root.dmbrs[0])

    queryfile = open(str(nr)+"rangequeries.txt","r")
    queries = json.load(queryfile)
    res = []
    totalTime = [0,0,0]
    totalNodesVisited = [0,0,0]
    totalDataPoints = [0,0,0]
    for i in range(0,len(queries)):
        arr = []
        arr2 = []
        arr3 = []
        query = queries[i]
        for dist in query:
            reslist = []
            start = time.time()
            nodesVisited = approx_range_search(root, dist, reslist, points[i], cdimen, ddimen, 0, k)
            end = time.time()
            arr2.append(end-start)
            arr3.append(nodesVisited)
            arr.append(len(reslist))
        res.append([arr,arr2,arr3])
        for j in range(0,3):
            totalDataPoints[j] += arr[j]
            totalTime[j] += arr2[j]
            totalNodesVisited[j] += arr3[j]
    avgtime = list()
    avgnodes = list()
    avgDataPoints = list()
    for j in range(0,3):
        avgtime.append(totalTime[j]/len(queries))
        avgnodes.append(totalNodesVisited[j]/len(queries))
        avgDataPoints.append(totalDataPoints[j]/len(queries))

    resultsfile = open("range_results.txt","a")
    resultsfile.write("k= "+str(k)+", "+str(nr)+"rectangles:"+"\n")
    resultsfile.write("Avg time: ")
    for j in range(0,3):
        resultsfile.write(str(avgtime[j])+" ")
    resultsfile.write("\n")
    resultsfile.write("Avg nodes visited: ")
    for j in range(0,3):
        resultsfile.write(str(avgnodes[j])+" ")
    resultsfile.write("\n")
    resultsfile.write("Avg data points: ")
    for j in range(0,3):
        resultsfile.write(str(avgDataPoints[j])+" ")
    resultsfile.write("\n")
    json.dump(res,outfile)
