import json
import time
import sys
import math

def calcMinDist(point, rectangle, dimen):
    mindist = 0
    for i in range(0,dimen):
        # r=point[i]
        # if point[i]<rectangle[i][0]:
        #     r = rectangle[i][0]
        # elif point[i]>rectangle[i][1]:
        #     r = rectangle[i][1]
        r = rectangle[i][0]
        mindist += math.pow(point[i][0]-r,2)
    return mindist

def nnsearch(point, reclist, dimen):
    res = sys.maxsize
    residx = 0
    i = 0
    for rec in reclist:
        x = calcMinDist(point,rec,dimen)
        if x<res:
            res = x
            residx = i
        i += 1
    return res,reclist[residx]

def seq_search_nn(nr):
    recfilename = str(nr)+"rectangles.txt"
    recfile = open(recfilename,"r")
    reclist = json.load(recfile)
    queriesfile = open(str(nr)+"nnqueries.txt","r")
    outfilename = str(nr)+"nnSeqSearchOutput.txt"
    outputfile = open(outfilename,"w")
    queries = json.load(queriesfile)
    dimen = len(reclist[0])
    res = []
    totalTime = 0
    errors = 0
    i = 0
    for point in queries:
        start = time.time()
        nearestdist, nearestRec = nnsearch(point, reclist, dimen)
        end = time.time()
        interval = end-start
        totalTime += interval
        res.append([interval, nearestdist, nearestRec])
    avgtime = totalTime/len(queries)
    # resfile.write(str(nr)+" rectangles: ")
    # resfile.write(str(avgtime)+'\n')
    json.dump(res, outputfile)
