import json
import pickle
import os

M = int(input("M value of R tree:"))
m = int(input("m value of R tree:"))

pol_file=open("policies.txt","r")
users_file=open("users.txt","r")
obj_file=open("objects.txt","r")
env_file=open("env.txt","r")

_,ua=int(users_file.readline().split())
_,ea=int(env_file.readline().split())
_,oa=int(obj_file.readline().split())
npol,nop=int(pol_file.readline().split())
dimen=ua+ea+oa+npol+1
pol_list=json.load(pol_file)

dict1={}
cnt=1
for i in range(0,ua):
    dict1['u'+str(i+1)]=cnt
    cnt+=1
for i in range(0,oa):
    dict1['o'+str(i+1)]=cnt
    cnt+=1
for i in range(0,ea):
    dict1['e'+str(i+1)]=cnt
    cnt+=1
dict1['op']=cnt
cnt+=1

rec_list=[]
for pol in pol_list:
    rec=[]
    for i in range(0,cnt):
        rec.append([])
    for x in pol:
        if pol[x]!=0:
            rec[dict1[x]-1]=[pol[x],pol[x]]
        elif x[0]=='u':
            rec[dict1[x]-1]=[1,ua]
        elif x[0]=='e':
            rec[dict1[x]-1]=[1,ea]
        else:
            rec[dict1[x]-1]=[1,oa]
    rec_list.append(rec)

file = open("rectangles.txt", "w")
json.dump(rec_list, file, indent=4)

file2 = open("rtreeparams.txt", "w")
file2.write(str(M)+' '+str(m))
file2.write('\n'+str(dimen)+'\n')