import json
import pickle
import random

class entity_list:
    def __init__(self):
        self.user_list=[]
        self.obj_list=[]
        self.env_list=[]

nquery=int(input("Enter no. of random queries:"))
user_file=open("users.txt","r")
obj_file=open("objects.txt","r")
env_file=open("env.txt","r")
pol_file=open("policies.txt","r")
entity_file=open("entity_sets.pkl","rb")

str1=user_file.readline()
words=str1.split()
nu=int(words[0])

str1=obj_file.readline()
words=str1.split()
no=int(words[0])

str1=env_file.readline()
words=str1.split()
ne=int(words[0])

str1=pol_file.readline()
words=str1.split()
np=int(words[0])
nops=int(words[1])

user_list=json.load(user_file)
obj_list=json.load(obj_file)
env_list=json.load(env_file)
pol_list=json.load(pol_file)

entity_sets=pickle.load(entity_file)
req_file=open("requests.txt","w")
req_list=[]
for i in range(0,nquery):
    j=random.randint(1,10)
    req=dict()
    print(j)
    if j<8:
        k=random.randint(0,np-1)
        while len(entity_sets[k].user_list)==0 or len(entity_sets[k].obj_list)==0 or len(entity_sets[k].env_list)==0:
            k=(k+1)%np
            if k<0:
                k+=np 
        r1=random.randint(0,len(entity_sets[k].user_list)-1)
        r2=random.randint(0,len(entity_sets[k].obj_list)-1)
        r3=random.randint(0,len(entity_sets[k].env_list)-1)

        x1=entity_sets[k].user_list[r1]
        x2=entity_sets[k].obj_list[r2]
        x3=entity_sets[k].env_list[r3]

        for i1 in x1:
            req[i1]=x1[i1]
        for i1 in x2:
            req[i1]=x2[i1]
        for i1 in x3:
            req[i1]=x3[i1]
            
        if pol_list[k]['op']!=0:
            req['op']=pol_list[k]['op']
        else:
            req['op']=random.randint(1,nops)

    else:
        r1=random.randint(0,nu-1)
        r2=random.randint(0,no-1)
        r3=random.randint(0,ne-1)
        
        for k in user_list[r1]:
            req[k]=user_list[r1][k]
        for k in obj_list[r2]:
            req[k]=obj_list[r2][k]
        for k in env_list[r3]:
            req[k]=env_list[r3][k]
        
        r4=random.randint(1,nops)
        req['op']=r4
    req_list.append(req)

json.dump(req_list,req_file,indent=4)