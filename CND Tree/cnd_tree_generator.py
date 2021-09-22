from cnd_tree_classes import *
from cds_functions import *
from ndds_functions import *
import sys

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

def GetMergedRectCDS(rec1, rec2, cdimen):
    rec3 = []
    for i in range(0,cdimen):
        rec3.append([min(rec1[i][0],rec2[i][0]), max(rec1[i][1],rec2[i][1])])
    return rec3

def GetMergedRectNDDS(rec1, rec2, ddimen):
    rec3 = []
    for i in range(0,ddimen):
        rec3.append(rec1[i].union(rec2[i]))
    return rec3

def ChooseLeaf(root, cds_lengths, ndds_lengths, cdimen, ddimen, rectangle):
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
            if rectangle.c_arr[j].issubset(rec[j]) == False:
                f=0
                break
        if f==1:
            cnt += 1
            idx.append(i)
        i += 1
    
    if cnt==1:
        return ChooseLeaf(root.children_[idx[0]], cds_lengths, ndds_lengths, cdimen, ddimen, rectangle)
    elif cnt>1:
        minarea = sys.maxsize
        idx1 = 0
        for j in idx:
            area = CalcAreaInCDS(root.cmbrs[j], cdimen, cds_lengths) * CalcAreaInNDDS(root.dmbrs[j], ddimen, ndds_lengths)
            if area<minarea:
                idx1 = j
                area = minarea
        return ChooseLeaf(root.children_[idx1], cds_lengths, ndds_lengths, cdimen, ddimen, rectangle)
    
    minOverlap = sys.maxsize
    n = len(root.dmbrs)
    idx_list = []
    for i in range(0,n):
        overlapArea = 0
        rec1 = GetMergedRectCDS(root.cmbrs[i], rectangle.c_arr, cdimen)
        rec2 = GetMergedRectNDDS(root.dmbrs[i], rectangle.d_arr, ddimen)
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
        return ChooseLeaf(root.children_[idx_list[0]], cds_lengths, ndds_lengths, cdimen, ddimen, rectangle)
    
    minEnlargement = sys.maxsize
    idx1 = -1
    for idx in idx_list:
        rec1 = GetMergedRectCDS(root.cmbrs[i], rectangle.c_arr, cdimen)
        rec2 = GetMergedRectNDDS(root.dmbrs[i], rectangle.d_arr, ddimen)
        area = CalcAreaInCDS(root.cmbrs[j], cdimen, cds_lengths) * CalcAreaInNDDS(root.dmbrs[j], ddimen, ndds_lengths)
        enlargedArea = CalcAreaInCDS(rec1, cdimen, cds_lengths) * CalcAreaInNDDS(rec2, ddimen, ndds_lengths)
        if enlargedArea - area <= minEnlargement:
            minEnlargement = enlargedArea - area
            idx1 = idx
    return ChooseLeaf(root.children_[idx1], cds_lengths, ndds_lengths, cdimen, ddimen, rectangle)

def Merge2D(rec1, rec2, cdim, ddim):
    mergedRec = []
    mergedRec.append(rec1[0].union(rec2[ddim]))
    mergedRec.append( [min(rec1[1][0], rec2[cdim][0]), max(rec1[1][1], rec2[cdim][1])] )
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
            m11 = d1.union(c1)
            m22 = d2.union(c2)
            m12 = d1.union(c2)
            m21 = d2.union(c1)
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
        max1 = max(max1, node.cmbrs[i][cdim][0])
        min1 = min(min1, node.cmbrs[i][cdim][1])
    cg1_2d.append(set_cg1)
    cg1_2d.append([min1, max1])
    min1 = -sys.maxsize
    max1 = sys.maxsize
    for i in cg2:
        set_cg2.union(node.dmbrs[i][ddim])
        max1 = max(max1, node.cmbrs[i][cdim][0])
        min1 = min(min1, node.cmbrs[i][cdim][1])
    cg2_2d.append(set_cg2)
    cg2_2d.append([min1, max1])
    cdim_length = cds_lengths[cdim]
    ddim_length = nds_lengths[ddim]
    area1 = calcArea2D(cg1_2d, cdim_length, ddim_length)
    area2 = calcArea2D(cg2_2d, cdim_length, ddim_length)
    perimeter1 = calcPerimeter2D(cg1_2d, cdim_length, ddim_length)
    perimeter2 = calcPerimeter2D(cg2_2d, cdim_length, ddim_length)

    for i in s1:
        rec = []
        rec.append(node.dmbrs[i][ddim])
        rec.append(node.cmbrs[i][cdim])
        merge1 = Merge2D(cg1_2d, rec, cdim, ddim)
        merge2 = Merge2D(cg2_2d, rec, cdim, ddim)
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

