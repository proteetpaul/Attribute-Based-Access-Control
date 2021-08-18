import time
import json
from rtree_util import calcMinDist

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
    outfilename = str(nr)+"rectangles_RangeSeqSearchOutput.txt"
    outputfile = open(outfilename,"w")
    resfile = open("RangeSeqSearchResults.txt","a")
    rtreefilename = str(nr)+"rectangles_rangeoutput.txt"
    rtreeoutfile = open(rtreefilename, "r")
    totaltime = 0
    dimen = len(reclist[0])
    outlist = []
    for query in queries:
        point = query[0]
        dist = query[1]
        start = time.time()
        reslist = calc(point, reclist, dimen, dist)
        end = time.time()
        interval = end-start
        totaltime += interval
        outlist.append([interval, len(reslist)])
    json.dump(outputfile, outlist)
    avgtime = totaltime/len(queries)
    resfile.write(str(nr)+" rectangles: "+str(avgtime))