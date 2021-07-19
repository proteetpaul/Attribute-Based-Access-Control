import json
import pickle
import os

M = int(input("M value of R tree:"))
m = int(input("m value of R tree:"))

pol_file = open("policies.txt", "r")
users_file = open("users.txt", "r")
obj_file = open("objects.txt", "r")
env_file = open("env.txt", "r")
values_file = open("values.txt", "r")

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
dimen = ua+ea+oa+1
pol_list = json.load(pol_file)

dict1 = {}
cnt = 1
for i in range(0, ua):
    dict1['u'+str(i+1)] = cnt
    cnt += 1
for i in range(0, oa):
    dict1['o'+str(i+1)] = cnt
    cnt += 1
for i in range(0, ea):
    dict1['e'+str(i+1)] = cnt
    cnt += 1
dict1['op'] = cnt

rec_list = []
for pol in pol_list:
    rec = []
    for i in range(0, cnt):
        rec.append([])
    for x in pol:
        if pol[x] != 0:
            rec[dict1[x]-1] = [pol[x], pol[x]]
        elif x == 'op':
            rec[dict1[x]-1] = [1, nop]
        else:
            rec[dict1[x]-1] = [1, nv]
    rec_list.append(rec)

file = open("rectangles.txt", "w")
json.dump(rec_list, file, indent=4)

file2 = open("rtreeparams.txt", "w")
file2.write(str(M)+' '+str(m))
file2.write('\n'+str(dimen)+'\n')
