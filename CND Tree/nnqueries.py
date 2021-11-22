import json
import sys
import math
import pickle
import random
from cnd_tree_classes import *

def generate_queries(nr, cdimen, ddimen):
    nqueries = 500
    cdsfile = open("cds_lengths.txt","r")
    cds_lengths = json.load(cdsfile)
    nddsfile = open("ndds_lengths.txt", "r")
    ndds_lengths = json.load(nddsfile)
    queries = []
    for i in range(0,nqueries):
        rec = hds_rectangle()
        x = 0
        y1 = 10000
        for j in range(0,cdimen):
            l = random.randint(x,y1)
            l/=100
            rec.c_arr.append([l,l])
        y2 = ndds_lengths[0]
        for j in range(0,ddimen):
            l2 = random.randint(1,y2)
            rec.d_arr.append(set([l2]))
        queries.append(rec)
    
    outfile = open(str(nr)+"nnqueries.pkl","wb")
    pickle.dump(queries, outfile)