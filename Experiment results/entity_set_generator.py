import pickle5 as pickle
import json
from poltree_classes import entity_list

def generate_entity_sets():
    users_file = open("users.txt", "r")
    objects_file = open("objects.txt", "r")
    env_file = open("env.txt", "r")
    pol_file = open("policies.txt", "r")

    pol_file.readline()
    objects_file.readline()
    env_file.readline()
    users_file.readline()
    policies = json.load(pol_file)
    users = json.load(users_file)
    envs = json.load(env_file)
    objects = json.load(objects_file)

    entity_sets=list()
    for pol in policies:
        e = entity_list()
        for user in users:
            f=1
            for x in user:
                if pol[x]!=user[x] and pol[x]!=0:
                    f=0
                    break
            if f==1:
                e.user_list.append(user)
        for obj in objects:
            f=1
            for x in obj:
                if pol[x]!=obj[x] and pol[x]!=0:
                    f=0
                    break
            if f==1:
                e.obj_list.append(obj)
        for env in envs:
            f=1
            for x in env:
                if pol[x]!=env[x] and pol[x]!=0:
                    f=0
                    break
            if f==1:
                e.env_list.append(obj)
        entity_sets.append(e)
    entityfile = open("entity_sets.pkl","wb")
    pickle.dump(entity_sets, entityfile, protocol = 4)
generate_entity_sets()