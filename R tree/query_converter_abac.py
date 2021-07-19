import json

pol_file=open("policies.txt","r")
users_file=open("users.txt","r")
obj_file=open("objects.txt","r")
env_file=open("env.txt","r")

query_file=open("queries.txt","r")
req_list1=json.load(query_file)
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

reqlist2=[]
for query in req_list1:
    rectangle=[]
    for i in range(0,cnt):
        rectangle.append([])
    for x in query:
        if query[x]!=0:
            rectangle[dict1[x]-1]=[query[x],query[x]]
        elif x[0]=='u':
            rectangle[dict1[x]-1]=[1,ua]
        elif x[0]=='e':
            rectangle[dict1[x]-1]=[1,ea]
        else: 
            rectangle[dict1[x]-1]=[1,oa]
    reqlist2.append(rectangle)

outfile = open("rtree_queries.txt","r")
json.dump(reqlist2, outfile)