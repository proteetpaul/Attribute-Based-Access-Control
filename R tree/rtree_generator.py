import json
import pickle
import random
import sys
import json
from anytree import NodeMixin, RenderTree

class node(NodeMixin):
    """ Class to represent rtree node """

    def __init__(self, id):
        super(node, self).__init__()
        self.id = id
        self.bounding_rectangles = list()
        self.children_ = list()
        self.isLeaf = True
        self.parent = None


inputfile = open("rectangles.txt", "r")
rectangle_set = json.load(inputfile)
inputfile2 = open("rtreeparams.txt", "r")
M, m = inputfile2.readline().split()
M = int(M)
m = int(m)
curid = 1
# Stores id of root during insertion
rootid = 0

nrectangles = len(rectangle_set)
if nrectangles == 0:
    exit
dimen = len(rectangle_set[0])

# function to calculate area of rectangle
def calcArea(rec):
    area = 1
    for i in range(0, dimen):
        area *= rec[i][1]-rec[i][0]
    return area

def ChooseLeaf(root, rectangle):
    if root.isLeaf:
        return root
    minEnlargement = sys.maxsize
    idx = 0
    j = 0
    for rec in root.bounding_rectangles:
        initialArea = calcArea(rec)
        enlargedArea = 1
        for i in range(0, dimen):
            enlargedArea *= (max(rec[i][1], rectangle[i]
                             [1]) - min(rec[i][0], rectangle[i][1]))
        if enlargedArea-initialArea < minEnlargement:
            minEnlargement = enlargedArea-initialArea
            idx = j
        j += 1
    return ChooseLeaf(root.children_[idx], rectangle)

# Choosing 2 entries that would waste most area if they were put together
def PickSeeds(n):
    maxarea = -1
    idx = []
    l = len(n.bounding_rectangles)
    for i in range(0, l):
        for j in range(i+1, l):
            area = 1
            for k in range(0, dimen):
                area *= (max(n.bounding_rectangles[i][k][1], n.bounding_rectangles[j][k][1]) -
                         min(n.bounding_rectangles[i][k][0], n.bounding_rectangles[j][k][0]))
            if area > maxarea:
                maxarea = area
                idx = [i, j]
    return idx

def PickNext(n, rec1, rec2):
    maxdiff = -1
    maxdiffidx = 0
    rec1area = calcArea(rec1)
    rec2area = calcArea(rec2)
    group = 1
    j = 0
    for rec in n.bounding_rectangles:
        enlargedarea1 = 1
        enlargedarea2 = 1
        for i in range(0, dimen):
            enlargedarea1 *= max(rec[i][1], rec1[i][1]) - \
                min(rec[i][0], rec1[i][0])
            enlargedarea2 *= max(rec[i][1], rec2[i][1]) - \
                min(rec[i][0], rec2[i][0])
        d1 = enlargedarea1-rec1area
        d2 = enlargedarea2-rec2area
        if abs(d1-d2) > maxdiff:
            maxdiffidx = j
            maxdiff = abs(d1-d2)
            group = 1
            if d1 > d2:
                group = 2
        j += 1
    return maxdiffidx, group

# Merge rec2 with rec1
def MergeRectangles(rec1, rec2):
    result = []
    for i in range(0, dimen):
        result.append([min(rec1[i][0], rec2[i][0]),
                      max(rec1[i][1], rec2[i][1])])
    return result

# Splits a node containing M+1 entries using quadratic cost algorithm
def SplitNode(n):
    global curid
    seeds = PickSeeds(n)
    l = node(n.id)
    ll = node(curid)
    curid += 1
    ll.parent = n.parent
    l.bounding_rectangles.append(n.bounding_rectangles[seeds[0]])
    ll.bounding_rectangles.append(n.bounding_rectangles[seeds[1]])
    l.isLeaf = n.isLeaf
    ll.isLeaf = n.isLeaf
    if n.isLeaf == 0:
        l.children_.append(n.children_[seeds[0]])
        ll.children_.append(n.children_[seeds[1]])
        n.children_.pop(seeds[1])
        n.children_.pop(seeds[0])
    rec1 = n.bounding_rectangles[seeds[0]]
    rec2 = n.bounding_rectangles[seeds[1]]
    n.bounding_rectangles.pop(seeds[1])
    n.bounding_rectangles.pop(seeds[0])

    len1 = 1
    len2 = 1
    while len1+len2 < M+1:
        cnt = len1+len2
        if (m-len1) == (M+1-cnt):
            while len1 < m:
                l.bounding_rectangles.append(n.bounding_rectangles[0])
                n.bounding_rectangles.pop(0)
                if n.isLeaf == 0:
                    l.children_.append(n.children_[0])
                    n.children_.pop(0)
                len1 += 1
            n.bounding_rectangles = l.bounding_rectangles
            n.children_ = l.children_
            for child in n.children_:
                child.parent = n
            for child in ll.children_:
                child.parent = ll
            return ll
        if (m-len2) == (M+1-cnt):
            while len2 < m:
                ll.bounding_rectangles.append(n.bounding_rectangles[0])
                n.bounding_rectangles.pop(0)
                if n.isLeaf == 0:
                    ll.children_.append(n.children_[0])
                    n.children_.pop(0)
                len2 += 1
            n.bounding_rectangles = l.bounding_rectangles
            n.children_ = l.children_
            for child in n.children_:
                child.parent = n
            for child in ll.children_:
                child.parent = ll
            return ll

        recidx, group = PickNext(n, rec1, rec2)
        rec = n.bounding_rectangles[recidx]
        n.bounding_rectangles.pop(recidx)
        if group == 1:
            l.bounding_rectangles.append(rec)
            rec1 = MergeRectangles(rec1, rec)
            len1 += 1
            if n.isLeaf == 0:
                l.children_.append(n.children_[recidx])
        else:
            ll.bounding_rectangles.append(rec)
            rec2 = MergeRectangles(rec2, rec)
            len2 += 1
            if n.isLeaf == 0:
                ll.children_.append(n.children_[recidx])
        if n.isLeaf == 0:
            n.children_.pop(recidx)
    n.bounding_rectangles = l.bounding_rectangles
    n.children_ = l.children_
    return ll

# Calculate bounding rectangle of a list of rectangles
def GetBoundingRectangle(reclist):
    global dimen
    rec = []
    for i in range(0, dimen):
        mx = reclist[0][i][1]
        mn = reclist[0][i][0]
        for rec1 in reclist:
            mx = max(mx, rec1[i][1])
            mn = min(mn, rec1[i][0])
        rec.append([mn, mx])
    return rec


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
        parent.bounding_rectangles[idx] = GetBoundingRectangle(
            l.bounding_rectangles)
        parent.children_[idx] = l
        if ll != None:
            parent.bounding_rectangles.append(
                GetBoundingRectangle(ll.bounding_rectangles))
            parent.children_.append(ll)
            if len(parent.bounding_rectangles) == M+1:
                pp = SplitNode(parent)
                for child in pp.children_:
                    child.parent = pp
                return AdjustTree(parent, pp, idx2)
        return AdjustTree(parent, None, idx2)
    else:
        if ll == None:
            return l
        newRoot = node(curid)
        rootid = curid
        curid += 1
        rec1 = GetBoundingRectangle(l.bounding_rectangles)
        rec2 = GetBoundingRectangle(ll.bounding_rectangles)
        newRoot.bounding_rectangles.append(rec1)
        newRoot.bounding_rectangles.append(rec2)
        newRoot.children_.append(l)
        newRoot.children_.append(ll)
        newRoot.isLeaf = False
        l.parent = newRoot
        ll.parent = newRoot
        return newRoot
    return None

def insert(root, rectangle):
    idx = -1
    l = ChooseLeaf(root, rectangle)
    idx = getParentIndex(l.parent, l)
    l.bounding_rectangles.append(rectangle)
    ll = None
    if len(l.bounding_rectangles) > M:
        ll = SplitNode(l)
    return AdjustTree(l, ll, idx)

root = node(0)
for rec in rectangle_set:
    root = insert(root, rec)
    for pre, _, node1 in RenderTree(root):
        x = len(node1.children_)
        print("%s%s %s" % (pre, str(node1.id), str(
            len(node1.bounding_rectangles))))
        print(node1.bounding_rectangles)
    print()
outputfile = open("rtree.pkl", "wb")
pickle.dump(root, outputfile, -1)
