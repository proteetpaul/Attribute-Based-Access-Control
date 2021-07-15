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
        
infile=open("poltree.pkl","rb")
node_list=pickle.load(infile)

#function to resolve an access request
def n_ary_resolve_any(curnode, access_req):
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
            decision=n_ary_resolve_any(node_list[curnode.children[i]],access_req)
            if decision=='allow':
                return 'allow'
        elif value==0:
            decision=n_ary_resolve_any(node_list[curnode.children[i]],access_req)
            if decision=='allow':
                return 'allow'
        i+=1
    # print("Exiting node with value 0")
    return 'deny'

req_file=open("requests.txt","r")
req_list=json.load(req_file)

for req in req_list:
    start=time.time()
    dec=n_ary_resolve_any(node_list[0],req)
    end=time.time()
    print(dec)
    print("time="+str(end-start))