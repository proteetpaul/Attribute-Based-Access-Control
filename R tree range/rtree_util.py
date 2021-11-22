import math

def calcMinDist(point, rectangle, dimen):
    mindist = 0
    for i in range(0,dimen):
        r=point[i][0]
        if point[i][0]<rectangle[i][0]:
            r = rectangle[i][0]
        elif point[i][0]>rectangle[i][1]:
            r = rectangle[i][1]
        mindist += math.pow(point[i][0]-r,2)
    return mindist