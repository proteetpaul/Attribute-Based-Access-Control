import json
import pickle
import random
from cnd_tree_classes import hds_rectangle

class entity_list:
    def __init__(self):
        self.user_list = []
        self.obj_list = []
        self.env_list = []

def generate_requests(nquery, nr):
    user_file=open(str(nr)+"users.txt","r")
    obj_file=open(str(nr)+"objects.txt","r")
    env_file=open(str(nr)+"env.txt","r")
    pol_file=open(str(nr)+"policies.txt","r")
    entity_file=open(str(nr)+"entity_sets.pkl","rb")
    entity_sets=pickle.load(entity_file)
    
    req_file=open(str(nr)+"requests.txt","w")

    _, uac, uad = user_file.readline().split()
    _, eac, ead = env_file.readline().split()
    _, oac, oad = obj_file.readline().split()
    uac = int(uac)
    eac = int(eac)
    oac = int(oac)
    uad = int(uad)
    ead = int(ead)
    oad = int(oad)
    dimen = uac+eac+oac+uad+ead+oad

    user_list=json.load(user_file)
    obj_list=json.load(obj_file)
    env_list=json.load(env_file)
    no = len(obj_list)
    nu = len(user_list)
    ne = len(env_list)
    np = nr
    requests = []

    for i in range(0, nquery):
        request = dict()
        o1 = random.randint(0, no-1)
        for j in obj_list[o1]:
            request[j] = obj_list[o1][j]
        u1 = random.randint(0, nu-1)
        while u1%np == o1:
            u1 = random.randint(0, nu-1)
        for j in user_list[u1]:
            request[j] = user_list[u1][j]
        e1 = random.randint(0, ne-1)
        while e1%np == o1:
            o1 = random.randint(0, ne-1)
        for j in env_list[e1]:
            request[j] = env_list[e1][j]
        requests.append(request)
    
    json.dump(requests, req_file)

def request_to_rectangle(nr):
    user_file=open(str(nr)+"users.txt","r")
    obj_file=open(str(nr)+"objects.txt","r")
    env_file=open(str(nr)+"env.txt","r")
    queries_file = open(str(nr)+"nnqueries.pkl","wb")
    req_file=open(str(nr)+"requests.txt","r")

    _, uac, uad = user_file.readline().split()
    _, eac, ead = env_file.readline().split()
    _, oac, oad = obj_file.readline().split()
    uac = int(uac)
    eac = int(eac)
    oac = int(oac)
    uad = int(uad)
    ead = int(ead)
    oad = int(oad)
    dimen = uac+eac+oac+uad+ead+oad

    user_list=json.load(user_file)
    obj_list=json.load(obj_file)
    env_list=json.load(env_file)
    requests = json.load(req_file)
    no = len(obj_list)
    nu = len(user_list)
    ne = len(env_list)

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
    for req in requests:
        rec = hds_rectangle()
        for i in range(0, cnt1-1):
            rec.c_arr.append([])
        for i in range(0, cnt2-1):
            rec.d_arr.append(set())
        for x in req:
            if x[1] == 'd':
                rec.d_arr[dict2[x]-1] = {req[x]}
            else:
                rec.c_arr[dict1[x]-1] = [req[x], req[x]]
        rec_list.append(rec)
    pickle.dump(rec_list, queries_file)
    