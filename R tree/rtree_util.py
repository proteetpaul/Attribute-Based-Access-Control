import math

def calcMinDist(point, rectangle, dimen):
    mindist = 0
    for i in range(0,dimen):
        r=point[i]
        if point[i]<rectangle[i][0]:
            r = rectangle[i][0]
        elif point[i]>rectangle[i][1]:
            r = rectangle[i][1]
        mindist += math.pow(point[i]-r,2)
    return mindist