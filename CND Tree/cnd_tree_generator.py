from cnd_tree_classes import *
from cds_functions import *
from ndds_functions import *
from anytree import RenderTree
import sys
import resource
import math
import json
import pickle

curid = 1
# Stores id of root during insertion
rootid = 0
cdimen = 0
ddimen = 0
cds_lengths = []
ndds_lengths = []
M, m = 0,0

def calcM():
    """ Function to calculate M value for R tree"""
    pagesize = resource.getpagesize() #Taking page size as 8kb
    recsize = (cdimen+ddimen) * 2 * 4
    ptrsize = 8 # Taking size of pointer as 8 bytes
    M = pagesize/(recsize + ptrsize)
    print(M)
    M = math.floor(M)
    m = math.floor(M/2)
    return M, m

def CalcAreaInCDS(rectangle, cdimen, cds_lengths):
    area = 1
    for i in range(0,cdimen):
        area *= (rectangle[i][1]-rectangle[i][0])/cds_lengths[i]
    return area

def CalcAreaInNDDS(rectangle, ddimen, hdds_lengths):
    area = 1
    for i in range(0, ddimen):
        area *= len(rectangle[i])/hdds_lengths[i]
    return area

def GetMergedRectCDS(rec1, rec2):
    rec3 = []
    for i in range(0,cdimen):
        rec3.append([min(rec1[i][0],rec2[i][0]), max(rec1[i][1],rec2[i][1])])
    return rec3

def GetMergedRectNDDS(rec1, rec2):
    rec3 = []
    for i in range(0,ddimen):
        rec3.append(rec1[i].union(rec2[i]))
    return rec3

def ChooseLeaf(root, rectangle):
    if root.isLeaf:
        return root
    cnt = 0
    idx = []
    i = 0
    for i in range(0,len(root.children_)):
        rec=root.dmbrs[i]
        f=1
        for j in range(0,ddimen):
            if rectangle.d_arr[j].issubset(rec[j]) == False:
                f=0
                break
        rec=root.cmbrs[i]
        for j in range(0,cdimen):
            # if rectangle.c_arr[j].issubset(rec[j]) == False:
            if rectangle.c_arr[j][0] <= rec[j][0] and rectangle.c_arr[j][1] >= rec[j][1]:
                f=0
                break
        if f==1:
            cnt += 1
            idx.append(i)
        i += 1
    
    if cnt==1:
        return ChooseLeaf(root.children_[idx[0]], rectangle)
    elif cnt>1:
        minarea = sys.maxsize
        idx1 = 0
        for j in idx:
            area = CalcAreaInCDS(root.cmbrs[j], cdimen, cds_lengths) * CalcAreaInNDDS(root.dmbrs[j], ddimen, ndds_lengths)
            if area<minarea:
                idx1 = j
                area = minarea
        return ChooseLeaf(root.children_[idx1], rectangle)
    
    minOverlap = sys.maxsize
    n = len(root.dmbrs)
    idx_list = []
    for i in range(0,n):
        overlapArea = 0
        rec1 = GetMergedRectCDS(root.cmbrs[i], rectangle.c_arr)
        rec2 = GetMergedRectNDDS(root.dmbrs[i], rectangle.d_arr)
        for j in range(0,n):
            if(j==i): continue
            overlapArea += OverlapInCDS(root.cmbrs[j], rec1, cdimen, cds_lengths) \
                * OverlapInNDDS(rec2,root.dmbrs[j], ddimen, ndds_lengths)
        if overlapArea < minOverlap:
            idx_list = [i]
            minOverlap = overlapArea
        elif overlapArea == minOverlap:
            idx_list.append(i)
    if len(idx_list)==1:
        return ChooseLeaf(root.children_[idx_list[0]], rectangle)
    
    minEnlargement = sys.maxsize
    idx1 = -1
    for idx in idx_list:
        rec1 = GetMergedRectCDS(root.cmbrs[i], rectangle.c_arr)
        rec2 = GetMergedRectNDDS(root.dmbrs[i], rectangle.d_arr)
        area = CalcAreaInCDS(root.cmbrs[j], cdimen, cds_lengths) * CalcAreaInNDDS(root.dmbrs[j], ddimen, ndds_lengths)
        enlargedArea = CalcAreaInCDS(rec1, cdimen, cds_lengths) * CalcAreaInNDDS(rec2, ddimen, ndds_lengths)
        if enlargedArea - area <= minEnlargement:
            minEnlargement = enlargedArea - area
            idx1 = idx
    return ChooseLeaf(root.children_[idx1], rectangle)

def Merge2D(rec1, rec2):
    mergedRec = []
    mergedRec.append(rec1[0].union(rec2[0]))
    mergedRec.append( [min(rec1[1][0], rec2[1][0]), max(rec1[1][1], rec2[1][1])] )
    return mergedRec

def calcPerimeter2D(rec, cdim_length, ddim_length):
    p = len(rec[0])/ddim_length + (rec[1][1]-rec[1][0])/cdim_length
    return p

def calcArea2D(rec, cdim_length, ddim_length):
    a = len(rec[0])/ddim_length * (rec[1][1]-rec[1][0])/ddim_length
    return a

def OverlapArea2D(rec1, rec2, cdim_length, ddim_length):
    if rec2[1][1]<=rec1[1][0] or rec1[1][1]<=rec2[1][0]:
        return 0
    a = len(rec1[0].union(rec2[0]))/ddim_length
    x = (min(rec1[1][1], rec2[1][1])-max(rec1[1][0], rec2[1][0]))/cdim_length
    return a*x

def CombinePartitions(cpartitions, dpartitions, node, M, cds_lengths, nds_lengths):
    # for x in cpartitions:
    #     print(x[0][0])
    #     print(x[0][1])
    # for x in dpartitions:
    #     print(x[0][0])
    #     print(x[0][1])
    maxMN = -sys.maxsize
    cg1 = set()
    cg2 = set()
    cdim = -1
    ddim = -1
    for x in cpartitions:
        c1=set(x[0][0])
        c2=set(x[0][1])
        for y in dpartitions:
            d1=set(y[0][0])
            d2=set(y[0][1])
            m11 = d1.intersection(c1)
            m22 = d2.intersection(c2)
            m12 = d1.intersection(c2)
            m21 = d2.intersection(c1)
            if len(m11) + len(m22) > maxMN:
                maxMN = len(m11) + len(m22)
                cg1 = m11
                cg2 = m22
                cdim = x[1]
                ddim = y[1]
            if len(m12) + len(m21) > maxMN:
                maxMN = len(m12) + len(m21)
                cg1 = m12
                cg2 = m21
                cdim = x[1]
                ddim = y[1]
    s1=set()
    for i in range(0,M+1):
        s1.add(i)
    s1.difference_update(cg1)
    s1.difference_update(cg2)
    #Redistributing uncommon entries
    minOverlap = sys.maxsize
    minRatio = sys.maxsize
    cg1_2d = []
    cg2_2d = []
    set_cg1 = set()
    set_cg2 = set()
    min1 = -sys.maxsize
    max1 = sys.maxsize
    for i in cg1:
        set_cg1.union(node.dmbrs[i][ddim])
        max1 = max(max1, node.cmbrs[i][cdim][1])
        min1 = min(min1, node.cmbrs[i][cdim][0])
    cg1_2d.append(set_cg1)
    cg1_2d.append([min1, max1])
    min1 = -sys.maxsize
    max1 = sys.maxsize
    for i in cg2:
        set_cg2.union(node.dmbrs[i][ddim])
        max1 = max(max1, node.cmbrs[i][cdim][1])
        min1 = min(min1, node.cmbrs[i][cdim][0])
    cg2_2d.append(set_cg2)
    cg2_2d.append([min1, max1])
    cdim_length = cds_lengths[cdim]
    ddim_length = nds_lengths[ddim]
    area1 = calcArea2D(cg1_2d, cdim_length, ddim_length)
    area2 = calcArea2D(cg2_2d, cdim_length, ddim_length)
    perimeter1 = calcPerimeter2D(cg1_2d, cdim_length, ddim_length)
    perimeter2 = calcPerimeter2D(cg2_2d, cdim_length, ddim_length)

    print(cg1)
    print(cg2)
    for i in s1:
        rec = []
        rec.append(node.dmbrs[i][ddim])
        rec.append(node.cmbrs[i][cdim])
        merge1 = Merge2D(cg1_2d, rec)
        merge2 = Merge2D(cg2_2d, rec)
        # Applying hs-5
        overlap1 = OverlapArea2D(merge1, cg2_2d, cdim_length, ddim_length)
        overlap2 = OverlapArea2D(merge2, cg1_2d, cdim_length, ddim_length)
        if overlap1 < overlap2:
            cg1_2d = merge1
            area1 = calcArea2D(cg1_2d, cdim_length, ddim_length)
            perimeter1 = calcPerimeter2D(cg1_2d, cdim_length, ddim_length)
            cg1.add(i)
            continue
        if overlap2 < overlap1:
            cg2_2d = merge2
            area2 = calcArea2D(cg2_2d, cdim_length, ddim_length)
            perimeter2 = calcPerimeter2D(cg2_2d, cdim_length, ddim_length)
            cg2.add(i)
            continue
        # Applying hs-6
        mergeArea1 = calcArea2D(merge1, cdim_length, ddim_length)
        mergeArea2 = calcArea2D(merge2, cdim_length, ddim_length)
        mergePerimeter1 = calcPerimeter2D(merge1, cdim_length, ddim_length)
        mergePerimeter2 = calcPerimeter2D(merge2, cdim_length, ddim_length)
        t1 = (mergePerimeter1-perimeter1)/(mergeArea1-area1)
        t2 = (mergePerimeter2-perimeter2)/(mergeArea2-area2)
        if t1 < t2 or (t1==t2 and len(cg1) < len(cg2)):
            cg1_2d = merge1
            area1 = calcArea2D(cg1_2d, cdim_length, ddim_length)
            perimeter1 = calcPerimeter2D(cg1_2d, cdim_length, ddim_length)
            cg1.add(i)
        else:
            cg2_2d = merge2
            area2 = calcArea2D(cg2_2d, cdim_length, ddim_length)
            perimeter2 = calcPerimeter2D(cg2_2d, cdim_length, ddim_length)
            cg2.add(i)
    return [cg1, cg2]

def SplitNode(node):
    global curid
    cds_partitions = list()
    for i in range(0,cdimen):
        cds_partitions.extend(SortEntries(node, i, cds_lengths[i], m, M))
    idx = SelectPartition(node, cds_partitions, cds_lengths, cdimen)
    bestCDSPartitions = []
    for i in idx:
        bestCDSPartitions.append(cds_partitions[i])

    ndds_partitions = ChoosePartitionSet(node, ndds_lengths, ddimen, m, M)
    idx1 = ChooseBestPartition(ndds_partitions, ndds_lengths, ddimen, node)
    bestNDDSPartitions = []
    for i in idx1:
        bestNDDSPartitions.append(ndds_partitions[i])
    bestPartition = CombinePartitions(bestCDSPartitions, bestNDDSPartitions, node, M, cds_lengths, ndds_lengths)
    l = cnd_tree_node(node.id)
    ll = cnd_tree_node(curid)
    ll.isLeaf = node.isLeaf
    ll.parent = node.parent

    curid += 1
    for i in bestPartition[0]:
        l.dmbrs.append(node.dmbrs[i])
        l.cmbrs.append(node.cmbrs[i])
        if node.isLeaf == False:
            l.children_.append(node.children_[i])
    for i in bestPartition[1]:
        ll.dmbrs.append(node.dmbrs[i])
        ll.cmbrs.append(node.cmbrs[i])
        if node.isLeaf == False:
            ll.children_.append(node.children_[i])
    node.cmbrs = l.cmbrs
    node.dmbrs = l.dmbrs
    node.children_ = l.children_
    return ll

def getParentIndex(parent, child):
    if parent == None:
        return -1
    j = 0
    for child_ in parent.children_:
        if child == child_:
            return j
        j += 1
    return -1

def AdjustTree(l, ll, idx):
    global curid
    parent = l.parent
    if parent != None:
        idx2 = getParentIndex(parent.parent, parent)
        parent.cmbrs[idx] = GetMBRInCDS(l.cmbrs, cdimen)
        parent.dmbrs[idx] = GetMBRInNDDS(l.dmbrs, ddimen)
        parent.children_[idx] = l
        if ll != None:
            parent.dmbrs.append(GetMBRInNDDS(ll.dmbrs, ddimen))
            parent.cmbrs.append(GetMBRInCDS(ll.cmbrs, cdimen))
            parent.children_.append(ll)
            if len(parent.dmbrs) == M+1:
                pp = SplitNode(parent)
                for child in pp.children_:
                    child.parent = pp
                return AdjustTree(parent, pp, idx2)
        return AdjustTree(parent, None, idx2)
    else:
        if ll == None:
            return l
        newRoot = cnd_tree_node(curid)
        rootid = curid
        curid += 1
        newRoot.cmbrs.append(GetMBRInCDS(l.cmbrs, cdimen))
        newRoot.dmbrs.append(GetMBRInNDDS(l.dmbrs, ddimen))
        newRoot.cmbrs.append(GetMBRInCDS(ll.cmbrs, cdimen))
        newRoot.dmbrs.append(GetMBRInNDDS(ll.dmbrs, ddimen))

        newRoot.children_.append(l)
        newRoot.children_.append(ll)
        newRoot.isLeaf = False
        l.parent = newRoot
        ll.parent = newRoot
        return newRoot
    return None

def insert(root, rec):
    l = ChooseLeaf(root, rec)
    idx = getParentIndex(l.parent, l)
    l.dmbrs.append(rec.d_arr)
    l.cmbrs.append(rec.c_arr)
    ll = None
    if len(l.dmbrs) == M+1:
        ll = SplitNode(l)
    return AdjustTree(l, ll, idx)

def build_rtree(nr):
    global curid, rootid, cdimen, ddimen, cds_lengths, ndds_lengths, M, m
    inputfilename = str(nr)+"rectangles.pkl"
    inputfile = open(inputfilename, "rb")
    cdsfile = open("cds_lengths.txt","r")
    cds_lengths = json.load(cdsfile)
    nddsfile = open("ndds_lengths.txt", "r")
    ndds_lengths = json.load(nddsfile)
    rectangle_set = pickle.load(inputfile)
    cdimen = len(cds_lengths)
    ddimen = len(ndds_lengths)

    nrectangles = len(rectangle_set)
    if nrectangles == 0:
        exit
    root = cnd_tree_node(0)
    M = 5
    m = 2
    print(str(M)+' '+str(m))
    for rec in rectangle_set:
        root = insert(root, rec)
        for pre, _, node1 in RenderTree(root):
            x = len(node1.children_)
            print("%s%s %s" % (pre, str(node1.id), str(len(node1.dmbrs)) ))
    print(curid)
    outputfile = open("cndtree.pkl", "wb")
    pickle.dump(root, outputfile, -1)
    outputfile.close()
    curid = 1
    rootid = 0

build_rtree(20)
# find nearest neighbour using sequential search then use the nn distance to generate range values