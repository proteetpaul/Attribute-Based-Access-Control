import json
import pickle
import os
from cnd_tree_classes import hds_rectangle

def convert_rectangles(nr):
    pol_file = open(str(nr)+"policies.txt", "r")
    users_file = open(str(nr)+"users.txt", "r")
    obj_file = open(str(nr)+"objects.txt", "r")
    env_file = open(str(nr)+"env.txt", "r")

    _, uac, uad = users_file.readline().split()
    _, eac, ead = env_file.readline().split()
    _, oac, oad = obj_file.readline().split()

    uac = int(uac)
    eac = int(eac)
    oac = int(oac)
    uad = int(uad)
    ead = int(ead)
    oad = int(oad)
    dimen = uac+eac+oac+uad+ead+oad
    pol_list = json.load(pol_file)
    npol = len(pol_list)

    dict1 = {}
    cnt1 = 1
    for i in range(0, uac):
        dict1['uc'+str(i+1)] = cnt1
        cnt1 += 1
    for i in range(0, oac):
        dict1['oc'+str(i+1)] = cnt1
        cnt1 += 1    
    for i in range(0, eac):
        dict1['ec'+str(i+1)] = cnt1
        cnt1 += 1

    dict2 = {}
    cnt2 = 1
    for i in range(0, uad):
        dict2['ud'+str(i+1)] = cnt2
        cnt2 += 1
    for i in range(0, oad):
        dict2['od'+str(i+1)] = cnt2
        cnt2 += 1
    for i in range(0, ead):
        dict2['ed'+str(i+1)] = cnt2
        cnt2 += 1
    
    rec_list = []
    for pol in pol_list:
        rec = hds_rectangle()
        for i in range(0, cnt1-1):
            rec.c_arr.append([])
        for i in range(0, cnt2-1):
            rec.d_arr.append(set())
        for x in pol:
            if x[1] == 'd':
                rec.d_arr[dict2[x]-1] = {pol[x]}
            else:
                rec.c_arr[dict1[x]-1] = [pol[x], pol[x]]
        rec_list.append(rec)

    file = open(str(nr)+"rectangles.pkl", "wb")
    pickle.dump(rec_list, file)
