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

def generate_data():
    nu = 5000 #int(input("Enter no. of users:"))
    no = 25000 #int(input("Enter no. of objects:"))
    ne = 20 #int(input("Enter no. of environment entities:"))
    ua = 20 #int(input("Enter no. of user attributes:"))
    oa = 20 #int(input("Enter no. of object attributes:"))
    ea = 2 #int(input("Enter no. of environment attributes:"))
    nvu = 100 #int(input("Enter no. of values of user attributes:"))
    nvo = 100 #int(input("Enter no. of values of objects attributes:"))
    nve = 10 #int(input("Enter no. of values of env attributes:"))
    np = int(input("Enter no. of policies:"))
    nops = 20 #int(input("Enter no. of ops:"))

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
            # Attribute value of 0 denotes *(any)
            arr[str1] = random.randint(0, nve)
        for j in range(0, ua):
            str1 = 'u'+str(j+1)
            arr[str1] = random.randint(0, nvu)
        for j in range(0, oa):
            str1 = 'o'+str(j+1)
            arr[str1] = random.randint(0, nvo)
        arr['op'] = random.randint(1, nops)

        if check_dup_policy(policies, arr):
            i -= 1
            continue
        policies.append(arr)

    pol_file = open("policies.txt", "w")
    pol_file.write(str(np)+' '+str(nops)+'\n')
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
                    if attrib[j] == 0:
                        attrib[j] = random.randint(0, nvu)
            entity_sets[i].user_list.append(attrib)
        else:
            x = random.randint(0, np-1)
            for j in policies[x]:
                if j[0] == 'u':
                    attrib[j] = policies[x][j]
                    if attrib[j] == 0:
                        attrib[j] = random.randint(0, nvu)
            entity_sets[x].user_list.append(attrib)
        user_list.append(attrib)

    obj_list = list()
    for i in range(0, no):
        attrib = dict()
        if i < np:
            for j in policies[i]:
                if j[0] == 'o' and j != 'op':
                    attrib[j] = policies[i][j]
                    if attrib[j] == 0:
                        attrib[j] = random.randint(0, nvo)
            entity_sets[i].obj_list.append(attrib)
        else:
            x = random.randint(0, np-1)
            for j in policies[x]:
                if j[0] == 'o' and j != 'op':
                    attrib[j] = policies[x][j]
                    if attrib[j] == 0:
                        attrib[j] = random.randint(0, nvo)
            entity_sets[x].obj_list.append(attrib)
        obj_list.append(attrib)

    env_list = list()
    for i in range(0, ne):
        attrib = dict()
        if i < np:
            for j in policies[i]:
                if j[0] == 'e':
                    attrib[j] = policies[i][j]
                    if attrib[j] == 0:
                        attrib[j] = random.randint(0, nve)
            entity_sets[i].env_list.append(attrib)
        else:
            x = random.randint(0, np-1)
            for j in policies[x]:
                if j[0] == 'e':
                    attrib[j] = policies[x][j]
                    if attrib[j] == 0:
                        attrib[j] = random.randint(0, nve)
            entity_sets[x].env_list.append(attrib)
        env_list.append(attrib)

    users_file = open("users.txt", "w")
    objects_file = open("objects.txt", "w")
    env_file = open("env.txt", "w")
    entity_set_file = open("entity_sets.pkl", "wb")
    values_file = open("values.txt", "w")

    # Writing required values to the files
    users_file.write(str(nu)+' '+str(ua)+'\n')
    objects_file.write(str(no)+' '+str(oa)+'\n')
    env_file.write(str(ne)+' '+str(ea)+'\n')
    values_file.write(str(nvu)+'\n'+str(nvo)+'\n'+str(nve)+'\n')

    # Dumping the lists of entities as json objects into the files
    json.dump(user_list, users_file, indent=4)
    json.dump(obj_list, objects_file, indent=4)
    json.dump(env_list, env_file, indent=4)

    # dumping the entity sets of each policy into a file
    pickle.dump(entity_sets, entity_set_file, -1)

generate_data()