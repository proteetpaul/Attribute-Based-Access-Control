import json

def query_converter_abac():
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
    nvu = int(values_file.readline())
    nvo = int(values_file.readline())
    nve = int(values_file.readline())
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

    reqlist2 = []
    for query in req_list1:
        rectangle = []
        for i in range(0, cnt):
            rectangle.append([])
        for x in query:
            if query[x]!=0:
                rectangle[dict1[x]-1] = [query[x], query[x]]
            elif x=='op':
                rectangle[dict1[x]-1] = [1, nop]
            elif x[0]=='o':
                rectangle[dict1[x]-1] = [1, nvo]
            elif x[0]=='e':
                rectangle[dict1[x]-1] = [1, nve]
            else:
                rectangle[dict1[x]-1] = [1, nvu]
        reqlist2.append(rectangle)

    outfile = open("rtree_queries.txt", "w")
    json.dump(reqlist2, outfile)

query_converter_abac()