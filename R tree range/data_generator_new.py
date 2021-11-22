import random
import json
import pickle

class entity_list:
    def __init__(self):
        self.user_list = []
        self.obj_list = []
        self.env_list = []

# function to check if randomly generated policy is a duplicate of an earlier generated policy
def check_dup_policy(policy_list, policy):
    for p in policy_list:
        f = 1
        for i in p:
            if p[i] != policy[i]:
                f = 0
                break
        if f == 1:
            return 1
    return 0

def generate_data(np):
    nu = min(5000,np) #int(input("Enter no. of users:"))
    no = np #int(input("Enter no. of objects:"))
    ne = 20
    ua = 6
    oa = 6
    ea = 2 
    nvu = 100 #int(input("Enter no. of values of user attributes:"))
    nvo = 100 #int(input("Enter no. of values of objects attributes:"))
    nve = 10 #int(input("Enter no. of values of env attributes:"))
    # nops = 20 #int(input("Enter no. of ops:"))

    # Building random policies
    print("Generating random policies...")
    policies = list()
    entity_sets = list()

    for i in range(0, np):
        arr = dict()
        arr2 = entity_list()
        entity_sets.append(arr2)
        for j in range(0, ea):
            str1 = 'e'+str(j+1)
            arr[str1] = random.randint(0, 10000)/100
        for j in range(0, ua):
            str1 = 'u'+str(j+1)
            arr[str1] = random.randint(0, 10000)/100
        for j in range(0, oa):
            str1 = 'o'+str(j+1)
            arr[str1] = random.randint(0, 10000)/100

        if check_dup_policy(policies, arr):
            i -= 1
            continue
        policies.append(arr)

    pol_file = open(str(np)+"policies.txt", "w")
    json.dump(policies, pol_file, indent=4)

    np = len(policies)
    # building user entities using generated policies
    print("Generating user, object and environment entities...")
    user_list = list()
    for i in range(0, nu):
        attrib = dict()
        if i < np:
            for j in policies[i]:
                if j[0] == 'u':
                    attrib[j] = policies[i][j]
            entity_sets[i].user_list.append(attrib)
        else:
            x = random.randint(0, np-1)
            for j in policies[x]:
                if j[0] == 'u':
                    attrib[j] = policies[x][j]
            entity_sets[x].user_list.append(attrib)
        user_list.append(attrib)

    obj_list = list()
    for i in range(0, no):
        attrib = dict()
        if i < np:
            for j in policies[i]:
                if j[0] == 'o':
                    attrib[j] = policies[i][j]
            entity_sets[i].obj_list.append(attrib)
        else:
            x = random.randint(0, np-1)
            for j in policies[x]:
                if j[0] == 'o':
                    attrib[j] = policies[x][j]
            entity_sets[x].obj_list.append(attrib)
        obj_list.append(attrib)

    env_list = list()
    for i in range(0, ne):
        attrib = dict()
        if i < np:
            for j in policies[i]:
                if j[0] == 'e':
                    attrib[j] = policies[i][j]
            entity_sets[i].env_list.append(attrib)
        else:
            x = random.randint(0, np-1)
            for j in policies[x]:
                if j[0] == 'e':
                    attrib[j] = policies[x][j]
            entity_sets[x].env_list.append(attrib)
        env_list.append(attrib)

    users_file = open(str(np)+"users.txt", "w")
    objects_file = open(str(np)+"objects.txt", "w")
    env_file = open(str(np)+"env.txt", "w")
    entity_set_file = open(str(np)+"entity_sets.pkl", "wb")

    # Writing required values to the files
    users_file.write(str(nu)+' '+str(ua)+'\n')
    objects_file.write(str(no)+' '+str(oa)+'\n')
    env_file.write(str(ne)+' '+str(ea)+'\n')

    # Dumping the lists of entities as json objects into the files
    json.dump(user_list, users_file, indent=4)
    json.dump(obj_list, objects_file, indent=4)
    json.dump(env_list, env_file, indent=4)

    # dumping the entity sets of each policy into a file
    pickle.dump(entity_sets, entity_set_file, -1)
