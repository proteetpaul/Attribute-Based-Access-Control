from cnd_tree_classes import *
import functools
import sys
from anytree import RenderTree

def cnt_elements(str1): # checked
    cnt = 0
    for c in str1:
        if c=='1':
            cnt+=1
    return cnt

def serialize_dset(s1, length):     # checked
    res=[]
    for i in range(0,length):
        res.append('0')
    for i in s1:
        res[i-1]='1'
    str1 = ""
    for c in res:
        str1 = str1+c
    return str1

def cset_compare(a,b):
    if cnt_elements(a[0])<cnt_elements(b[0]):
        return -1
    elif cnt_elements(a[0])>cnt_elements(b[0]):
        return 1
    else:
        if a[1]>b[1]:
            return -1
        return 1

def contains1(set1, string1):   # checked
    """ Function to check if both set1 and string1(serialised form) contain a common element """
    for x in set1:
        if str(string1[x-1])=='1':
            return 1
    return 0

def union1(set1, string1):  # checked
    """ Function to return union of a set and a serialised set (?)"""
    set2 = set1.copy()
    for i in range(0,len(string1)):
        if string1[i] == '1':
            set2.add(i+1)
    return set2

def UnionStrings(string1, string2): # checked
    """ Calculates union of 2 serialised sets """
    arr = []
    n = len(string1)
    for i in range(0,n):
        if string1[i]=='1' or string2[i] == '1':
            arr.append('1')
        else:
            arr.append('0')
    string3 = ""
    for i in arr:
        string3 = string3 + i
    return string3

def IntersectionStrings(string1, string2):      # checked
    """ Calculates intersection of 2 serialised sets """
    n = len(string1)
    res = 0
    for i in range(0,n):
        if string1[i]=='1' and string2[i]=='1':
            res+=1
    return res

def CalcIntersectionSum(ml):        # checked
    """ Calculate sum of intersections obtained by placing a crossing set at a particular position """
    prefix_sets = [ml[0]]
    suffix_sets = [ml[-1]]
    n = len(ml)
    for i in range(1,n):
        prefix_sets.append(UnionStrings(prefix_sets[i-1], ml[i]))
    j = 0
    for i in range(n-2,-1,-1):
        suffix_sets.append(UnionStrings(suffix_sets[j], ml[i]))
        j += 1
    res=0
    for i in range(0,n-1):
        res+=IntersectionStrings(prefix_sets[i], suffix_sets[n-2-i])
    return res
    
def UnionAll(arr, length):  # checked
    """ Calculate union of serialised sets present in arr"""
    res=""
    res1 = list()
    for i in range(0,length):
        res1.append('0')
    for s in arr:
        for i in range(0,length):
            if s[i]=='1':
                res1[i]='1'
    for c in res1:
        res = res+c
    return res

def GetMBRInNDDS(reclist, dimen):   # checked
    rec = []
    for i in range(0,dimen):
        s1 = set()
        for x in reclist:
            s1=s1.union(x[i])
        rec.append(s1)
    return rec

def BuildAuxTree(node, d, length):  # checked
    n = len(node.dmbrs)
    l = set()
    f = list()
    for i in range(0,n):
        l = l.union(node.dmbrs[i][d])
    # initialize forest F with single-node trees, one tree T for each l ∈ L
    for letter in l:
        t = aux_tree_node()
        t.letters.add(letter)
        f.append(t)
    #sorting all Dth component sets by size in ascending order and break ties by frequency in descending order
    dict1 = dict()
    for s in node.dmbrs:
        x = serialize_dset(s[d], length)
        if x in dict1:
            dict1[x] += 1
        else:
            dict1[x] = 1
    sl = list()
    for key,value in dict1.items():
        sl.append([key, value])
    cmp_key = functools.cmp_to_key(cset_compare)
    sl = sorted(sl, key = cmp_key)

    for i in range(0,len(sl)):
        idx_list = []
        j = 0
        for t in f:
            check = contains1(t.letters, sl[i][0])
            if check == 1:
                idx_list.append(j)
            j += 1
        if len(idx_list)==1:
            t=f[idx_list[0]]
            t.letters = union1(t.letters, sl[i][0])
            t.sets.add(sl[i][0])
            t.freq += sl[i][1]
            f[idx_list[0]] = t
            continue
        t1 = aux_tree_node()
        t1.letters = union1(set(),sl[i][0])
        t1.sets.add(sl[i][0])
        t1.freq += sl[i][1]
        f1 = list()
        for j in range(0,len(f)):
            if j not in idx_list:
                f1.append(f[j])
            else:
                t=f[j]
                t1.freq += t.freq
                t1.sets = t1.sets.union(t.sets)
                t1.letters = t1.letters.union(t.letters)
                t.parent = t1
        f1.append(t1)
        f = f1.copy()
    if len(f)>1:
        newroot = aux_tree_node()
        for t in f:
            t.parent = newroot
            newroot.letters = newroot.letters.union(t.letters)
            newroot.sets = newroot.sets.union(t.sets)
            newroot.freq += t.freq
        return newroot
    return f[0]

def SortComponentSets(t, length):   # checked
    if t.height == 0:
        return list(t.sets) 
    l1 = list()
    l2 = list()
    w1 = w2 = 0
    dict1 = dict()
    # Arranging subtrees in list based on frequencies
    s1=list(t.children)
    s1=sorted(s1, key=lambda x: x.freq, reverse = False)         # check with reverse order
    for x in s1:
        if x.freq > 0:
            if w1<w2:
                w1+=x.freq
                l1.append(UnionAll(x.sets, length))
            else:
                w2+=x.freq
                l2.append(UnionAll(x.sets, length))
    l2.reverse()
    # Concatenating l1 and l2
    ml = l1 + l2
    crossing_sets = set()
    # Generating crossing sets
    for s2 in t.sets:
        cnt = 0
        idx1 = []
        j = 0
        for t1 in t.children:
            if contains1(t1.letters, s2) == 1:
                cnt+=1
                idx1.append(j)
            j += 1
        if cnt>1:
            crossing_sets.add(s2)
        else:
            t.children[idx1[0]].sets.add(s2)
    for set1 in crossing_sets:
        n=len(ml)
        idx=-1
        minIntersectionSum = sys.maxsize
        for i in range(1,n):
            ml1 = ml[:i]
            ml1.append(set1)
            ml1 = ml1+ml[i:]
            x = CalcIntersectionSum(ml1)
            if x < minIntersectionSum:
                idx = i
                minIntersectionSum = x
        arr = ml.copy()
        ml = arr[:idx]
        ml.append(set1)
        ml = ml + arr[idx:]
    i = 0
    # res_ml = ml.copy()
    res_ml = []
    # print('len(ml)= '+str(len(ml)))
    # print('crossing sets= '+str(crossing_sets))
    # for t1 in s1:
    #     # Check here
    #     if len(t1.sets) == 0 or t1.freq == 0:
    #         continue
    #     set_list1 = SortComponentSets(t1,length)
    #     x = UnionAll(t1.sets, length)
    #     print(x)
    #     while i < len(ml) and x!=ml[i]:
    #         res_ml.append(ml[i])
    #         i+=1
    #     res_ml=res_ml+set_list1
    #     i+=1

    for x in ml:
        if x in crossing_sets:
            res_ml.append(x)
            continue
        for t1 in s1:
            if len(t1.sets) == 0 or t1.freq == 0:
                continue
            y = UnionAll(t1.sets, length)
            if y == x:
                set_list1 = SortComponentSets(t1,length)
                res_ml = res_ml + set_list1
                break
    # print(len(res_ml))
    return res_ml

def ChoosePartitionSet(node, ndds_lengths, ddimen, m, M):   # checked
    """ Choose partition sets for ndds for all dimenions"""
    partition_set = list()
    # print('dmbrs = '+str(node.dmbrs))
    for i in range(0,ddimen):
        dict1 = dict()
        length = ndds_lengths[i]
        for j in range(0,len(node.dmbrs)):
            x = serialize_dset(node.dmbrs[j][i], length)
            if x in dict1:
                dict1[x].append(j)
            else:
                dict1[x]=[j]
        aux_tree = BuildAuxTree(node, i, length)
        # for pre, _, node1 in RenderTree(aux_tree):
        #     x = len(node1.children_)
        #     print("%s %s %s" % (pre, str(node1.letters), str(node1.sets) ))
        csets_list = SortComponentSets(aux_tree, length)
        entry_set = []
        for x in csets_list:
            for i1 in dict1[x]:
                entry_set.append(i1)
        # print(len(entry_set))
        for j in range(m,M-m+2):
            p1=[]
            p2=[]
            for i1 in range(0,j):
                p1.append(entry_set[i1])
            for i1 in range(j,M+1):
                p2.append(entry_set[i1])
            p=[p1,p2]
            partition_set.append([p,i])
    return partition_set

def OverlapInNDDS(rec1, rec2, ddimen, ndds_lengths):        # checked
    area = 1
    for i in range(0,ddimen):
        area*=len(rec1[i].intersection(rec2[i]))/ndds_lengths[i]
    return area

def ChooseBestPartition(partition_set, ndds_lengths, ddimen, node):     # checked
    """ Select best partition among chosen partitions """
    minOverlap = sys.maxsize
    maxSpan = 0
    minBalance = sys.maxsize
    idx = []
    x = GetMBRInNDDS(node.dmbrs, ddimen)
    for i in range(0,len(partition_set)):
        p = partition_set[i][0]
        list1 = []
        list2 = []
        for j in p[0]:
            list1.append(node.dmbrs[j])
        for j in p[1]:
            list2.append(node.dmbrs[j])

        p1 = GetMBRInNDDS(list1, ddimen)
        p2 = GetMBRInNDDS(list2, ddimen)
        dimen = partition_set[i][1]
        overlap = OverlapInNDDS(p1, p2, ddimen, ndds_lengths)
        span = len(x[dimen])
        balance = abs(len(p1[dimen])-len(p2[dimen])) #max(len(p1[dimen]), len(p2[dimen])) / min(len(p1[dimen]), len(p2[dimen]))
        # Applying hs-1
        if overlap < minOverlap:
            minOverlap = overlap
            maxSpan = span
            minBalance = balance
            idx = [i]
        elif overlap == minOverlap:
            # Applying hs-2
            if span > maxSpan:
                minOverlap = overlap
                maxSpan = span
                minBalance = balance
                idx = [i]
            # Applying hs-3
            elif span == maxSpan and balance < minBalance:
                minOverlap = overlap
                maxSpan = span
                minBalance = balance
                idx = [i]
            elif span == maxSpan and balance == minBalance:
                idx.append(i)
    return idx