import math 
import json
import pickle

#represents a user entity
class user:
    def __init__(self,id):
        self.id=id
        self.attrib=dict()

#represents an object entity
class object:
    def __init__(self,id):
        self.id=id
        self.attrib=dict()

#represents an environment entity
class env:
    def __init__(self,id):
        self.id=id
        self.attrib=dict()

#represents a node of the policy tree
class node:
    def __init__(self,id):
        self.id=id
        self.attrib=None
        self.value_list=[]
        self.children=[]
        self.decision='deny'
        self.op=''

#represents a list of entities, used to generate the policy tree
class entity_list:
    def __init__(self):
        self.user_list=[]
        self.obj_list=[]
        self.env_list=[]

#list of nodes of poltree
node_list=list()
cnt=0
#function to generate n-ary policy tree
def gen_poltree(avp_list,attrib_set,pol_list,entities):
    #attrib_set=attrib_set1.copy()
    #print(attrib_set)
    global cnt
    curnode=node(cnt)
    cnt+=1
    node_list.append(curnode)
    if len(attrib_set)==0:
        curnode.decision='allow'
        curnode.op=pol_list[0]['op']
        node_list[curnode.id]=curnode
        # print("Exiting leaf node")
        return curnode.id
    
    nu=len(entities.user_list)
    no=len(entities.obj_list)
    ne=len(entities.env_list)
    #print(str(nu)+' '+str(no)+' '+str(ne))
    p=[]

    for i in avp_list:
        x=0.0
        for ue in entities.user_list:
            if i[0] in ue.attrib and ue.attrib[i[0]]==i[1]:
                x=x+1.0/nu
        for oe in entities.obj_list :
            if i[0] in oe.attrib and oe.attrib[i[0]]==i[1]:
                x=x+1.0/no
        for ee in entities.env_list:
            if i[0] in ee.attrib and ee.attrib[i[0]]==i[1]:
                x=x+1.0/ne 
        if x>0:
            p.append([i[0],i[1],x])
    
    max_entropy=-1.0
    max_attrib=''
    for attrib in attrib_set:
        entropy=0.0
        for x in p:
            if x[0]==attrib:
                entropy-=x[2]*(math.log(x[2])/math.log(2))
        if entropy>max_entropy:
            max_entropy=entropy
            max_attrib=attrib
    
    # print(max_attrib)
    curnode.attrib=max_attrib
    attrib_set.remove(max_attrib)

    #finding set of values corresponding to maxattrib
    value_set=set()
    avp_list2=list()
    value_set.add(0)
    for i in avp_list:
        if i[0]==max_attrib:
            value_set.add(i[1])
        else:
            avp_list2.append(i)

    #print(value_set)
    #generating policy sets of children nodes
    pol_sets=[]
    for value in value_set:
        arr=list()
        
        for pol in pol_list:
            if pol[max_attrib]==value:
                arr.append(pol)
        #print(len(arr))
        if len(arr):
            pol_sets.append(arr)
            curnode.value_list.append(value)
    
    #generating entity sets of children nodes
    entity_sets=[]
    for arr in pol_sets:
        arr2=entity_list()
        for ue in entities.user_list:
            f=0
            for policy in arr:
                f1=1
                for i in policy:
                    if i in ue.attrib and policy[i]!=ue.attrib[i]:
                        f1=0
                        break
                if f1==1:
                    f=1
                    break
            if f==1:
                arr2.user_list.append(ue)
            
        for oe in entities.obj_list:
            f=0
            for policy in arr:
                f1=1
                for i in policy:
                    if i in oe.attrib and policy[i]!=oe.attrib[i]:
                        f1=0
                        break
                if f1==1:
                    f=1
                    break
            if f==1:
                arr2.obj_list.append(oe)

        for ee in entities.env_list:
            f=0
            for policy in arr:
                f1=1
                for i in policy:
                    if i in ee.attrib and policy[i]!=ee.attrib[i]:
                        f1=0
                        break
                if f1==1:
                    f=1
                    break
            if f==1:
                arr2.env_list.append(ee)
        entity_sets.append(arr2)
    
    i=0
    for value in curnode.value_list:
        x=0
        if len(pol_sets[i])>0:
            # print('value=',value)
            # print('No. of policies=',len(pol_sets[i]))
            x=gen_poltree(avp_list2,attrib_set.copy(),pol_sets[i],entity_sets[i])
            curnode.children.append(x)
        i+=1

    node_list[curnode.id]=curnode
    #print('Exiting node with max attribute '+max_attrib)
    return curnode.id

users_file=open("users.txt","r")
objects_file=open("objects.txt","r")
env_file=open("env.txt","r")
pol_file=open("policies.txt","r")

str1=users_file.readline()
words=str1.split()
nu=int(words[0])
ua=int(words[1])

str1=objects_file.readline()
words=str1.split()
no=int(words[0])
oa=int(words[1])

str1=env_file.readline()
words=str1.split()
ne=int(words[0])
ea=int(words[1])

str1=pol_file.readline()
words=str1.split()
np=int(words[0])
nops=int(words[1])

avp_list=list()

arr2=json.load(users_file)
# loading list of users from json file
user_list=list()
for i in range(0,nu):
    ui=user(i+1)
    ui.attrib=arr2[i]
    user_list.append(ui)
    for j in arr2[i]:
        if [j,arr2[i][j]] not in avp_list:
            avp_list.append([j,arr2[i][j]])

#loading list of objects from json file
arr2=json.load(objects_file)
obj_list=list()
for i in range(0,no):
    oi=object(i+1)
    oi.attrib=arr2[i]
    obj_list.append(oi)
    for j in arr2[i]:
        if [j,arr2[i][j]] not in avp_list:
            avp_list.append([j,arr2[i][j]])

# loading list of environment entities from json file
arr2=json.load(env_file)
env_list=list()
for i in range(0,ne):
    ei=env(i+1)
    ei.attrib=arr2[i]
    env_list.append(ei)
    for j in arr2[i]:
        if [j,arr2[i][j]] not in avp_list:
            avp_list.append([j,arr2[i][j]])

# loading list of policies from json file
policies=json.load(pol_file)

attrib_set=set()
for i in range(0,ua):
    attrib_set.add('u'+str(i+1))
for i in range(0,oa):
    attrib_set.add('o'+str(i+1))
for i in range(0,ea):
    attrib_set.add('e'+str(i+1))

entities=entity_list()
entities.user_list=user_list
entities.obj_list=obj_list
entities.env_list=env_list

gen_poltree(avp_list,attrib_set,policies,entities)
print(len(node_list))
outfile=open("poltree.pkl","wb")
pickle.dump(node_list,outfile,-1)

