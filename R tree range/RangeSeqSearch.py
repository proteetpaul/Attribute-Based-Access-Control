import time
import json
from rtree_util import calcMinDist
import math

def calc(point, reclist, dimen, dist):
    reslist = []
    for rec in reclist:
        if calcMinDist(point, rec, dimen) <= dist:
            reslist.append(rec)
    return reslist

def range_search(nr):
    recfilename = str(nr)+"rectangles.txt"
    recfile = open(recfilename,"r")
    reclist = json.load(recfile)
    queriesfile = open("rangequeries.txt","r")
    queries = json.load(queriesfile)
    # file1=open("range2.txt","w")
    outfilename = str(nr)+"rectangles_RangeSeqSearchOutput.txt"
    outputfile = open(outfilename,"w")
    resfile = open("RangeSeqSearchResults.txt","a")
    totaltime = 0
    totalqueries = 0
    dimen = len(reclist[0])
    # ploty=[]
    res = []
    for query in queries:
        querylist=query[1]
        point=query[0]
        arr=[]
        for i in range(0,len(querylist)):
            dist = querylist[i]
            start = time.time()
            reslist = calc(point, reclist, dimen, dist)
            end = time.time()
            interval = end-start
            totaltime += interval
            arr.append([len(reslist),interval])
            # ploty.append(math.log10(interval))
            # outlist.append([interval, len(reslist)])
        res.append(arr)
        totalqueries += len(querylist)
    json.dump(res,outputfile)
    avgtime = totaltime/totalqueries
    resfile.write(str(nr)+" rectangles: "+str(avgtime)+'\n')
    # json.dump(ploty,file1)