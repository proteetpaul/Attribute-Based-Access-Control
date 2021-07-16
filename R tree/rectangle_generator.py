import random
import json
import pickle

def check_dup_rectangle(rectangle_set, rectangle, dimen):
    for r in rectangle_set:
        f = 1
        for i in range(0, dimen):
            if rectangle[i] != r[i]:
                f = 0
                break
        if f == 1:
            return True
    return False

choice = int(input("Enter 1 for normal rectangle and 2 for point rectangles:"))
M = int(input("M value of R tree:"))
m = int(input("m value of R tree:"))
dimen = int(input("Enter no. of dimensions:"))
nrectangles = int(input("Enter no. of rectangles:"))
limits = []
print("Enter upper and lower bounds for each dimension:")
for i in range(0, dimen):
    x, y = input("Dimen "+str(i+1)+":").split()
    limits.append([int(x), int(y)])

rectangle_set = []
for i in range(0, nrectangles):
    rectangle = []
    for j in range(0, dimen):
        if choice == 1:
            l = random.randint(limits[j][0], limits[j][1]-1)
            u = random.randint(l+1, limits[j][1])
        else:
            l = random.randint(limits[j][0], limits[j][1])
            u = l
        rectangle.append([l, u])
    if(check_dup_rectangle(rectangle_set, rectangle, dimen)):
        i -= 1
        continue
    rectangle_set.append(rectangle)

file = open("rectangles.txt", "w")
json.dump(rectangle_set, file, indent=4)

file2 = open("rtreeparams.txt", "w")
file2.write(str(M)+' '+str(m))
file2.write('\n'+str(dimen)+'\n')
json.dump(limits, file2, indent=4)
