import json
import pickle
import time
from bin_poltree_node import node

def binary_resolve_any(root, request):
    if root.is_leaf:
        f=1
        y=root.avp_list
        for x in y:
            if request[x]!=y[x] and y[x]!=0 and request[x]!=0:
                f=0
                break
        if f==1:
            return 'Yes'
        return 'No'
    x=root.attrib
    if request[x]==root.value or request[x] == 0:
        if root.left != None:
            return binary_resolve_any(root.left, request)
    if request[x]!=root.value or request[x]==0:
        if root.right!=None:    
            return binary_resolve_any(root.right, request)
    return 'No'

def resolve():
    infile=open("bin_poltree.pkl","rb")
    root=pickle.load(infile)

    req_file=open("requests.txt","r")
    req_list=json.load(req_file)
    outfile = open("bin_poltree_output.txt","w")
    resultsfile = open("bin_poltree_results.txt","a")
    reslist = []

    nallowed = 0
    ndenied = 0
    totalTimeAllowed = 0
    totalTimeDenied = 0
    checkfile = open("results.txt","r")
    check = json.load(checkfile)
    i=0
    f=0
    falseneg = 0
    falsepos = 0
    for req in req_list:
        start=time.time()
        dec=binary_resolve_any(root,req)
        end=time.time()
        reslist.append([dec, end-start])  
        if check[i][1] != dec:
            f+=1
            if dec == 'Yes':
                falsepos += 1
            else:
                falseneg += 1
        if dec=='Yes':
            totalTimeAllowed += end-start
            nallowed += 1
        else:
            totalTimeDenied += end-start
            ndenied += 1
        i+=1

    avgTimeAllowed = totalTimeAllowed/nallowed
    avgTimeDenied = totalTimeDenied/ndenied
    avgTime = (totalTimeAllowed + totalTimeDenied)/(nallowed + ndenied)
    list1 = [avgTimeAllowed, avgTimeDenied, avgTime]
    json.dump(list1, resultsfile, indent = 4)
    json.dump(reslist, outfile, indent = 4)
    print(f)
    print(falsepos)
    print(falseneg)

resolve()