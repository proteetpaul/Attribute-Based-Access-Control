import random
import json
import pickle
from cnd_tree_classes import hds_rectangle

def generate_rectangles(nr, cdimen, ddimen):
    reclist = []
    cds_lengths = []
    ndds_lengths = []
    for i in range(0,nr):
        rec = hds_rectangle()
        x = 0
        y1 = 10000
        for j in range(0,cdimen):
            l = random.randint(x,y1)
            l/=100
            rec.c_arr.append([l,l])
        y2 = 10
        for j in range(0,ddimen):
            l2 = random.randint(1,y2)
            rec.d_arr.append(set([l2]))
        reclist.append(rec)

    for i in range(0,cdimen):
        cds_lengths.append(100)
    for i in range(0,ddimen):
        ndds_lengths.append(10)
        
    filename = str(nr)+"rectangles.pkl"
    file = open(filename, "wb")
    pickle.dump(reclist, file)
    cdsfile = open("cds_lengths.txt","w")
    json.dump(cds_lengths, cdsfile)
    nddsfile = open("ndds_lengths.txt", "w")
    json.dump(ndds_lengths, nddsfile)

generate_rectangles(20, 2, 2)
