import json
import pickle
import time

#represents a node of the policy tree
class node:
    def __init__(self,id):
        self.id=id
        self.attrib=None
        self.value_list=[]
        self.children=[]
        self.decision='deny'
        self.op=''
        

#function to resolve an access request
def n_ary_resolve_any(curnode, access_req, node_list):
    # print("Entering node with attrib ",curnode.attrib)
    if curnode.decision=='allow':
        if access_req['op']==curnode.op:
            return 'allow'
        else: 
            return 'deny'
    i=0
    decision='deny'
    for value in curnode.value_list:
        if value==access_req[curnode.attrib]:
            decision=n_ary_resolve_any(node_list[curnode.children[i]],access_req, node_list)
            if decision=='allow':
                return 'allow'
        elif value==0:
            decision=n_ary_resolve_any(node_list[curnode.children[i]],access_req, node_list)
            if decision=='allow':
                return 'allow'
        i+=1
    # print("Exiting node with value 0")
    return 'deny'

def resolve(np):
    infile=open("poltree.pkl","rb")
    node_list=pickle.load(infile)

    req_file=open("requests.txt","r")
    req_list=json.load(req_file)
    outfilename = str(np)+"policies_poltree_output.txt"
    outfile = open(outfilename,"w")
    resultsfile = open("poltree_results.txt","a")
    reslist = []

    nallowed = 0
    ndenied = 0
    totalTimeAllowed = 0
    totalTimeDenied = 0
    for req in req_list:
        start=time.time()
        dec=n_ary_resolve_any(node_list[0],req, node_list)
        end=time.time()
        reslist.append([dec, end-start])  
        if dec=='allow':
            totalTimeAllowed += end-start
            nallowed += 1
        else:
            totalTimeDenied += end-start
            ndenied += 1

    avgTimeAllowed = totalTimeAllowed/nallowed
    avgTimeDenied = totalTimeDenied/ndenied
    avgTime = (totalTimeAllowed + totalTimeDenied)/(nallowed + ndenied)
    list1 = [avgTimeAllowed, avgTimeDenied, avgTime]
    resultsfile.write(str(np)+' policies')
    json.dump(list1, resultsfile, indent = 4)
    json.dump(reslist, outfile, indent = 4)

