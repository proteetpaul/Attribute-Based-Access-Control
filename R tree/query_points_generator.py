import json
import random

def gen_query_points():
    inputfile2 = open("rtreeparams.txt", "r")
    inputfile2.readline()
    dimen = int(inputfile2.readline())
    limits = json.load(inputfile2)
    x = limits[0]
    y = limits[1]
    points = []
    for i in range(0,1):
        p = list()
        for j in range(0,dimen):
            l = random.randint(x, y)
            p.append(l)
        points.append(p)
    outfile = open("nnqueries.txt","w")
    json.dump(points, outfile, indent = 4)