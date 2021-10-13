import json
import time
import sys
import math
import pickle
from cnd_tree_classes import *

def calcDist(p1, rec, cdimen, ddimen):
    t = 0.01
    dist = 0
    for i in range(0,cdimen):
        x=p1.c_arr[i][0]
        y=rec.c_arr[i]
        if x<y[0]-t or x>y[1]+t:
            dist += 1
    for i in range(0,ddimen):
        x = p1.d_arr[i]
        if x.issubset(rec.d_arr[i]) == False:
            dist += 1
    return dist

def nnsearch(point, reclist, cdimen, ddimen):
    res = sys.maxsize
    residx = 0
    i = 0
    for rec in reclist:
        x = calcDist(point,rec,cdimen, ddimen)
        if x<res:
            res = x
            residx = i
        i += 1
    return res,reclist[residx]

def seq_search_nn(nr):
    recfilename = str(nr)+"rectangles.pkl"
    recfile = open(recfilename,"rb")
    reclist = pickle.load(recfile)
    queriesfile = open("nnqueries.pkl","rb")
    outfilename = str(nr)+"rectangles_nnSeqSearchOutput.txt"
    outputfile = open(outfilename,"w")
    queries = pickle.load(queriesfile)
    cdimen = len(reclist[0].c_arr)
    ddimen = len(reclist[0].d_arr)
    res = []
    i = 0
    for point in queries:
        nearestdist, nearestRec = nnsearch(point, reclist, cdimen, ddimen)
        res.append(nearestdist)
    
    json.dump(res, outputfile)