import pickle
import json
import math

def maxrange(point, dimen):
    sum=0
    for i in range(0,dimen):
        if point[i]>=50 :
            sum = sum + math.pow(point[i]-100,2)
        else:
            sum += math.pow(point[i],2)
    return sum 

def generate_queries(nr):
    nnfilename = str(nr)+"rectanglesNNSearchOutput.txt"
    nnfile = open(nnfilename, "r")
    nnres = json.load(nnfile)
    queryfile = open("nnqueries.txt","r")
    queries = json.load(queryfile)
    outfile = open("rangequeries.txt","w")
    rangequeries=[]
    dimen = len(queries[0])
    k=5
    for i in range(0,len(queries)):
        x=nnres[i][1]
        x+=k*dimen
        rangequeries.append([queries[i],x])
    json.dump(rangequeries, outfile, indent = 4)

def generate_queries2(nr):
    nnfilename = str(nr)+"rectanglesNNSearchOutput.txt"
    nnfile = open(nnfilename, "r")
    nnres = json.load(nnfile)
    queryfile = open("nnqueries.txt","r")
    queries = json.load(queryfile)
    outfile = open("rangequeries.txt","w")
    rangequeries=[]
    dimen = len(queries[0])
    k=5
    for i in range(0,len(queries)):
        arr=[]
        x=nnres[i][1]
        arr.append(x/2)
        arr.append(x)
        y=x*2
        sum = maxrange(queries[i],dimen)
        while y<=sum:
            arr.append(y)
            y*=2
        arr.append(y)
        rangequeries.append([queries[i],x])
    json.dump(rangequeries, outfile, indent = 4)
    
