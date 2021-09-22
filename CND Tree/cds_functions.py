from cnd_tree_classes import *
import sys

def SortEntries(node, d, length, m, M):
    arr = []
    for i in range(0,M+1):
        arr.append([node[i], i])
    arr = sorted(arr, key=lambda x: x[0][d][0])
    partitions = list()
    for i in range(m,M-m+1):
        p1=[]
        for j in range(0,i):
            p1.append(arr[j][1])
        p2=[]
        for j in range(i,M+1):
            p2.append(arr[j][1])
        p = [[p1,p2],d]
        partitions.add(p)
    return partitions

def OverlapInCDS(rec1, rec2, cdimen, cds_lengths):
    area = 1
    for i in range(0, cdimen):
        if rec1[i][1]<=rec2[i][0] or rec1[i][0]>=rec2[i][1]:
            return 0
        area *= (min(rec1[i][1],rec2[i][1]) - min(rec1[i][0],rec2[i][0])) / cds_lengths[i]
    return area

def GetMBRInCDS(reclist, cdimen):
    mbr = []
    for i in range(0, cdimen):
        min1 = sys.maxsize
        max1 = -sys.maxsize
        for rec in reclist:
            min1 = min(rec[i][0], min1)
            max1 = max(rec[i][1], max1)
        mbr.append([min1, max1])
    return mbr

def SelectPartition(partition_set, cds_lengths, cdimen):
    # Applying hs1: minimum overlap
    idx=[]
    minOverlap = sys.maxsize
    balance = list()
    for i in range(0,len(partition_set)):
        p = partition_set[i][0]
        p1 = GetMBRInCDS(p[0], cdimen)
        p2 = GetMBRInCDS(p[1], cdimen)
        # Calculating balance (to be used later in hs3)
        dim = partition_set[i][1]
        y1 = p1[dim][1]-p1[dim][0]
        y2 = p2[dim][1]-p2[dim][0]
        balance.append(max(y1,y2)/min(y1,y2))
        x = OverlapInCDS(p1, p2, cdimen, cds_lengths)
        if x < minOverlap:
            idx = [i]
            minOverlap = x
        elif x==minOverlap:
            idx.append(i)
    if len(idx) == 1:
        return idx
    # Applying hs2: maximum span
    idx2 = []
    max_cds_length = 0
    for i in idx:
        dim = partition_set[i][1]
        if cds_lengths[dim]>max_cds_length:
            max_cds_length=cds_lengths[i]
            idx2=[i]
        elif cds_lengths[dim]==max_cds_length:
            idx2.append(i)
    if len(idx2) == 1:
        return idx2
    # Applying hs3: maximum balance
    minbalance = sys.maxsize
    idx3 = []
    for i in idx2:
        if balance[i] < minbalance:
            minbalance = balance[i]
            idx3 = [i]
        elif balance[i] == minbalance:
            idx3.append(i)
    return idx3

