import json
import time
import sys
import math
import pickle
from cnd_tree_classes import *
from nearest_neighbor_search import calcDist

def seq_range_search(nr):
    recfilename = str(nr)+"rectangles.pkl"
    recfile = open(recfilename,"rb")
    rectangles = pickle.load(recfile)
    treefile = open("cndtree.pkl","rb")
    root = pickle.load(treefile)
    outfilename = str(nr)+"rectangles_range_seq_output.txt"
    outfile = open(outfilename, "w")
    infilename = str(nr)+"rectangles_rangeoutput.txt"
    infile = open(infilename, "r")
    rangeres = json.load(infile)
    nnqueryfile = open("nnqueries.pkl","rb")
    points = pickle.load(nnqueryfile)
    cdimen = len(root.cmbrs[0])
    ddimen = len(root.dmbrs[0])

    queryfile = open("rangequeries.txt","r")
    queries = json.load(queryfile)
    res = []
    totalTime = [0,0,0]
    totalDataPoints = [0,0,0]
    errors = 0
    for i in range(0,len(queries)):
        arr = []
        arr2 = []
        query = queries[i]
        for dist in query:
            start = time.time()
            cnt = 0
            for rec in rectangles:
                if calcDist(points[i], rec, cdimen, ddimen) <= dist:
                    cnt+=1
            end = time.time()
            arr.append(cnt)
            arr2.append(end-start)
        res.append([arr,arr2])

        if arr!=rangeres[i]:
            errors += 1
        res.append(arr)

    avgtime = list()
    avgDataPoints = list()
    for j in range(0,3):
        avgtime.append(totalTime[j]/len(queries))
        avgDataPoints.append(totalDataPoints[j]/len(queries))

    resultsfile = open(str(nr)+"range_results_seq.txt","w")
    resultsfile.write(str(nr)+"rectangles"+"\n")
    resultsfile.write("Avg time: ")
    for j in range(0,3):
        resultsfile.write(str(avgtime[j]))
    resultsfile.write("\n")
    resultsfile.write("Avg data points: ")
    for j in range(0,3):
        resultsfile.write(str(avgDataPoints[j]))
    resultsfile.write("\n")

    json.dump(res, outfile)
    print(errors)