import json
import time
import nearest_neighbor
import pickle
from rtree_util import calcMinDist
from rtree_node import node
import matplotlib.pyplot as plt
import math

def range_search(node, dist, reslist, point, dimen, nodesVisited):
    k = 1 + 0.5 * node.height
    nodesVisited += 1
    if node.isLeaf == 1:
        for rec in node.bounding_rectangles:
            if calcMinDist(point, rec, dimen) <= dist:
                reslist.append(rec)
        return nodesVisited
    n = len(node.bounding_rectangles)
    for i in range(0,n):
        if calcMinDist(point, node.bounding_rectangles[i], dimen) * k <= dist:
            nodesVisited = range_search(node.children_[i], dist, reslist, point, dimen, nodesVisited)
    return nodesVisited
    
def range_queries(nr):
    queryfile = open("rangequeries.txt","r")
    rtreefile = open("rtree.pkl","rb")
    outfilename = str(nr)+"rectangles_approxrangeoutput.txt"
    outfile = open(outfilename, "w")
    resfile = open("ApproxRangeResults_RTree.txt","a")
    root = pickle.load(rtreefile)
    dimen = len(root.bounding_rectangles[0])
    queries=json.load(queryfile)
    res=[]
    res2=[]
    totaltime = 0
    totalqueries = 0
    totalnodesVisited = 0
    num_points_arr = [0,0,0]
    cnt = [0,0,0]
    time_interval_arr = [0,0,0]
    nodes_arr = [0,0,0]
    for query in queries:
        querylist=query[1]
        point=query[0]
        arr=[]
        for i in range(0,min(3,len(querylist))):
            dist = querylist[i]
            reslist = []
            start = time.time()
            nodesVisited = 0
            nodesVisited = range_search(root, dist, reslist, point, dimen, nodesVisited)
            end = time.time()
            totalnodesVisited += nodesVisited
            interval=end-start
            totaltime += interval
            arr.append([len(reslist), interval, nodesVisited])
            num_points_arr[i] += len(reslist)
            time_interval_arr[i] += interval
            nodes_arr[i] += nodesVisited
            cnt[i] += 1
        res.append(arr)
        totalqueries += len(querylist)
    avgtime = totaltime / totalqueries
    avgNodesVisited = totalnodesVisited / totalqueries
    json.dump(res, outfile)
    # resfile.write(str(nr) + " rectangles: " + str(avgtime) + ' ' + str(avgNodesVisited) + '\n')
    resfile.write(str(nr) + " rectangles: \n")
    for i in range(0,3):
        nodes_arr[i] /= cnt[i]
        num_points_arr[i] /= cnt[i]
        time_interval_arr[i] /= cnt[i]
        resfile.write(str(nodes_arr[i])+' '+str(num_points_arr[i])+' '+str(time_interval_arr[i])+'\n')

    # outfile=open("plot_arrays.txt","w")
    # p1=[plotx,ploty]
    # json.dump(p1,outfile)
