import json
import time
import nearest_neighbor
import pickle
from rtree_util import calcMinDist
from rtree_node import node
import matplotlib.pyplot as plt

def range_search(node, dist, reslist, point, dimen):
    if node.isLeaf == 1:
        for rec in node.bounding_rectangles:
            if calcMinDist(point, rec, dimen) <= dist:
                reslist.append(rec)
        return
    n = len(node.bounding_rectangles)
    for i in range(0,n):
        if calcMinDist(point, node.bounding_rectangles[i], dimen) <= dist:
            range_search(node.children_[i], dist, reslist, point, dimen)
    
def range_queries(nr):
    queryfile = open("RangeQueries.txt","r")
    rtreefile = open("rtree.pkl","rb")
    # outfilename = str(nr)+"rectangles_rangeoutput.txt"
    # outfile = open(outfilename, "w")
    # resfile = open("RangeResults_RTree.txt","a")
    root = pickle.load(rtreefile)
    dimen = len(root.bounding_rectangles[0])
    queries=json.load(queryfile)
    res=[]
    res2=[]
    totaltime = 0
    query=queries[0]
    point=query[0]
    plotx = []
    ploty = []
    for i in range(1,len(query)):
        dist = query[i]
        reslist = []
        start = time.time()
        range_search(root, dist, reslist, point, dimen)
        end = time.time()
        interval=end-start
        totaltime += interval
        plotx.append(dist)
        ploty.append(len(reslist))
        # res2.append([len(reslist), interval])
        # res.append(reslist)
    # avgtime = totaltime/len(queryfile)
    # json.dump(res2, outfile)
    # resfile.write(str(nr)+" rectangles: "+str(avgtime))
    plt.plot(plotx,ploty)
    plt.show()
