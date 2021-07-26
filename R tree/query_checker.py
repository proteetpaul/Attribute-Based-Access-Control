import json
import time

def query_checker(query, req_list1):
    f1=0
    for pol in pol_list:
        f=1
        for x in pol:
            if pol[x]==0 or query[x]==0:
                continue
            if pol[x]!=query[x]:
                f=0
                break
        if f==1:
            f1=1
            break
    return f1

pol_file = open("policies.txt", "r")

query_file = open("requests.txt", "r")
req_list1 = json.load(query_file)
npol, nop = pol_file.readline().split()
pol_list = json.load(pol_file)

resfile=open("results.txt","w")
resultsFile = open("seq_search_results.txt", "a")
res=[]
nallowed = 0
ndenied = 0
totalTimeAllowed = 0
totalTimeDenied = 0
for query in req_list1:
    start=time.time()
    f1 = query_checker(query,req_list1)
    end = time.time()
    timeTaken = end-start
    if f1==1:
        res.append([timeTaken, "Yes"])
        nallowed += 1
        totalTimeAllowed += timeTaken
    else :
        res.append([timeTaken, "No"])
        ndenied += 1
        totalTimeDenied += timeTaken
json.dump(res,resfile,indent=4)

avgTimeAllowed = totalTimeAllowed/nallowed
avgTimeDenied = totalTimeDenied/ndenied
avgTime = (totalTimeAllowed + totalTimeDenied)/(nallowed + ndenied)
list1 = [avgTimeAllowed, avgTimeDenied, avgTime]
json.dump(list1, resultsFile, indent = 4)