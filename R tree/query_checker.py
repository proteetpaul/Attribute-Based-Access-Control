import json

pol_file = open("policies.txt", "r")
users_file = open("users.txt", "r")
obj_file = open("objects.txt", "r")
env_file = open("env.txt", "r")
values_file = open("values.txt", "r")

query_file = open("requests.txt", "r")
req_list1 = json.load(query_file)
_, ua = users_file.readline().split()
_, ea = env_file.readline().split()
_, oa = obj_file.readline().split()
npol, nop = pol_file.readline().split()

ua = int(ua)
ea = int(ea)
oa = int(oa)
npol = int(npol)
nop = int(nop)
nv = int(values_file.readline())
pol_list = json.load(pol_file)

resfile=open("results.txt","w")
res=[]
for query in req_list1:
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
    if f1==1:
        res.append("Yes")
    else :
        res.append("No")
json.dump(res,resfile)
