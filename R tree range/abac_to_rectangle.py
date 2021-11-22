import json
import pickle
import os

def convert_rectangles(nr):
    pol_file = open(str(nr)+"policies.txt", "r")
    users_file = open(str(nr)+"users.txt", "r")
    obj_file = open(str(nr)+"objects.txt", "r")
    env_file = open(str(nr)+"env.txt", "r")

    _, ua = users_file.readline().split()
    _, ea = env_file.readline().split()
    _, oa = obj_file.readline().split()

    ua = int(ua)
    ea = int(ea)
    oa = int(oa)
    dimen = ua+ea+oa
    pol_list = json.load(pol_file)
    npol = len(pol_list)

    dict1 = {}
    cnt1 = 1
    for i in range(0, ua):
        dict1['u'+str(i+1)] = cnt1
        cnt1 += 1
    for i in range(0, oa):
        dict1['o'+str(i+1)] = cnt1
        cnt1 += 1    
    for i in range(0, ea):
        dict1['e'+str(i+1)] = cnt1
        cnt1 += 1
    
    rec_list = []
    for pol in pol_list:
        rec = []
        for i in range(0, cnt1-1):
            rec.append([])
        for x in pol:
            rec[dict1[x]-1] = [pol[x], pol[x]]
        rec_list.append(rec)

    file = open(str(nr)+"rectangles.txt", "w")
    json.dump(rec_list, file)
