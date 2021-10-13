import json
import time
import sys
import math
import pickle
from cnd_tree_classes import *

def generate_queries(nr):
    nnfilename = str(nr)+"rectangles_nnSeqSearchOutput.txt"
    nnfile = open(nnfilename, "r")
    nnres = json.load(nnfile)
    queryfile = open("nnqueries.pkl","rb")
    queries = pickle.load(queryfile)
    outfile = open("rangequeries.txt","w")
    rangequeries=[]
    maxdist = int(input("Enter maxdist value: "))

    for i in range(0,len(queries)):
        arr = []
        arr.append(nnres[i]-1)
        arr.append(nnres[i])
        arr.append(nnres[i]+1)
        # for j in range(nnres+1, maxdist):
        #     arr.append(j)
        rangequeries.append(arr)
    
    json.dump(rangequeries, outfile, indent = 4)
        