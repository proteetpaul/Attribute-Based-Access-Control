import math
import json
import pickle
import sys
from anytree import RenderTree
from bin_poltree_node import node
from poltree_classes import *

class entity_dict:
    def __init__(self):
        self.user_dict=dict()
        self.obj_dict=dict()
        self.env_dict=dict()

cnt = 0
def getEntitySet(entities, pol_list, edict_list, idx_list):
    arr2 = entity_list()
    for ue in entities.user_list:
        for i in idx_list:
            x1 = frozenset(ue.attrib.values())
            if edict_list[i].user_dict.get(x1) == True:
                arr2.user_list.append(ue)
                break
    #     f = 0
    #     for policy in pol_list:
    #         f1 = 1
    #         for i in policy:
    #             if i in ue.attrib and policy[i] != ue.attrib[i]:# and policy[i] != 0:
    #                 f1 = 0
    #                 break
    #         if f1 == 1:
    #             f = 1
    #             break
    #     if f == 1:
    #         arr2.user_list.append(ue)

    for oe in entities.obj_list:
        for i in idx_list:
            x1 = frozenset(oe.attrib.values())
            if edict_list[i].obj_dict.get(x1) == True:
                arr2.obj_list.append(oe)
                break
    #     f = 0
    #     for policy in pol_list:
    #         f1 = 1
    #         for i in policy:
    #             if i in oe.attrib and policy[i] != oe.attrib[i]:# and policy[i] != 0:
    #                 f1 = 0
    #                 break
    #         if f1 == 1:
    #             f = 1
    #             break
    #     if f == 1:
    #         arr2.obj_list.append(oe)

    for ee in entities.env_list:
        for i in idx_list:
            x1 = frozenset(ee.attrib.values())
            if edict_list[i].env_dict.get(x1) == True:
                arr2.env_list.append(ee)
                break
    #     f = 0
    #     for policy in pol_list:
    #         f1 = 1
    #         for i in policy:
    #             if i in ee.attrib and policy[i] != ee.attrib[i]:# and policy[i] != 0:
    #                 f1 = 0
    #                 break
    #         if f1 == 1:
    #             f = 1
    #             break
    #     if f == 1:
    #         arr2.env_list.append(ee)
    return arr2

def gen_binpoltree(avp, entities, pol_list, edict_list, idx_list):
    global cnt
    curnode = node(cnt)
    cnt += 1
    if len(pol_list) == 1:
        pol = pol_list[0]
        for x in pol:
            for y in avp:
                if x == y[0] and pol[x] == y[1]:
                    curnode.avp_list[x] = pol[x]
        curnode.avp_list['op'] = pol['op']
        return curnode

    nu = len(entities.user_list)
    no = len(entities.obj_list)
    ne = len(entities.env_list)

    freq_list = [0]*len(avp)
    i = 0
    max_attrib = None
    max_val = None
    max_freq = -1.0
    for x in avp:
        x1, x2 = x[0], x[1]
        if x1[0] == 'u':
            for user in entities.user_list:
                if user.attrib[x1] == x2:
                    freq_list[i] += 1.0/nu
        elif x1[0] == 'o':
            for obj in entities.obj_list:
                if obj.attrib[x1] == x2:
                    freq_list[i] += 1.0/no
        else:
            for env in entities.env_list:
                if env.attrib[x1] == x2:
                    freq_list[i] += 1.0/ne
        if freq_list[i] > max_freq and freq_list[i]<1:
            max_attrib = x1
            max_val = x2
            max_freq = freq_list[i]
        i += 1
    # print(max_attrib+' '+str(max_val))
    curnode.attrib = max_attrib
    curnode.value = max_val
    # generating policy sets of children nodes
    Py = []
    Pn = []
    idx_list1 = []
    idx_list2 = []
    i = 0
    for pol in pol_list:
        if pol[max_attrib] == max_val or pol[max_attrib] == 0:
            Py.append(pol)
            idx_list1.append(idx_list[i])
        if pol[max_attrib] != max_val or pol[max_attrib] == 0:
            Pn.append(pol)
            idx_list2.append(idx_list[i])
        i+=1
    avp.remove([max_attrib, max_val])
    # generating entity sets of children nodes
    ey = getEntitySet(entities, Py, edict_list, idx_list)
    en = getEntitySet(entities, Pn, edict_list, idx_list)
    if len(Py)>0:
        curnode.left = gen_binpoltree(avp.copy(), ey, Py, edict_list, idx_list1)
        curnode.left.parent = curnode
    if len(Pn)>0:
        curnode.right = gen_binpoltree(avp.copy(), en, Pn, edict_list, idx_list2)
        curnode.right.parent = curnode
    return curnode

def generator():
    users_file = open("users.txt", "r")
    objects_file = open("objects.txt", "r")
    env_file = open("env.txt", "r")
    pol_file = open("policies.txt", "r")
    entities_file = open("entity_sets.pkl","rb")

    entity_sets = pickle.load(entities_file)

    str1 = users_file.readline()
    words = str1.split()
    nu = int(words[0])
    ua = int(words[1])

    str1 = objects_file.readline()
    words = str1.split()
    no = int(words[0])
    oa = int(words[1])

    str1 = env_file.readline()
    words = str1.split()
    ne = int(words[0])
    ea = int(words[1])

    str1 = pol_file.readline()
    words = str1.split()
    np = int(words[0])
    nops = int(words[1])

    avp_list = list()

    arr2 = json.load(users_file)
    # loading list of users from json file
    user_list = list()
    for i in range(0, nu):
        ui = user(i+1)
        ui.attrib = arr2[i]
        user_list.append(ui)
        for j in arr2[i]:
            if [j, arr2[i][j]] not in avp_list:
                avp_list.append([j, arr2[i][j]])

    # loading list of objects from json file
    arr2 = json.load(objects_file)
    obj_list = list()
    for i in range(0, no):
        oi = object(i+1)
        oi.attrib = arr2[i]
        obj_list.append(oi)
        for j in arr2[i]:
            if [j, arr2[i][j]] not in avp_list:
                avp_list.append([j, arr2[i][j]])

    # loading list of environment entities from json file
    arr2 = json.load(env_file)
    env_list = list()
    for i in range(0, ne):
        ei = env(i+1)
        ei.attrib = arr2[i]
        env_list.append(ei)
        for j in arr2[i]:
            if [j, arr2[i][j]] not in avp_list:
                avp_list.append([j, arr2[i][j]])

    # loading list of policies from json file
    policies = json.load(pol_file)

    entities = entity_list()
    entities.user_list = user_list
    entities.obj_list = obj_list
    entities.env_list = env_list

    edict_list = list()
    idx_list = list(range(0,np))
    for e in entity_sets:
        x = entity_dict()
        for ue in e.user_list:
            x1 = frozenset(ue.values())
            x.user_dict[x1]=True
        for oe in e.obj_list:
            x1 = frozenset(oe.values())
            x.obj_dict[x1] = True
        for ee in e.env_list:
            x1 = frozenset(ee.values())
            x.env_dict[x1] = True
        edict_list.append(x)

    root = gen_binpoltree(avp_list, entities, policies, edict_list, idx_list)
    # for pre, _, node1 in RenderTree(root):
    #     print("%s%s %s %s" % (pre, node1.id,node1.attrib,node1.value))

    outfile = open("bin_poltree.pkl", "wb")
    pickle.dump(root, outfile, -1)
