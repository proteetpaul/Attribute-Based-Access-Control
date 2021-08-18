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
        mindist += math.pow(point[i]-r,2)
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
    queriesfile = open("nnqueries.txt","r")
    outfilename = str(nr)+"rectangles_nnSeqSearchOutput.txt"
    outputfile = open(outfilename,"w")
    resfile = open("nnSeqSearchResults.txt","a")
    infilename = str(nr)+"rectanglesNNSearchOutput.txt"
    infile = open(infilename,"r")
    queries = json.load(queriesfile)
    dimen = len(reclist[0])
    res = []
    res2 = json.load(infile)
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
        if res2[i][1]!=res[i][1] or res2[i][2]!=res[i][2]:
            errors+=1
    avgtime = totalTime/len(queries)
    print(errors)
    resfile.write(str(nr)+" rectangles: ")
    resfile.write(str(avgtime)+'\n')
    json.dump(res, outputfile)
