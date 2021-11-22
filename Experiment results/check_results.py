import json

poltreefile = open("100policies_poltree_output.txt","r")
rtreefile = open("100policies_rtree_output.txt","r")
seqsearchfile = open("100policies_seq_search_output.txt","r")
res1=json.load(poltreefile)
res2=json.load(rtreefile)
res3=json.load(seqsearchfile)
f1,f2=0,0
i=0
m=dict()
m['allow']='Yes'
m['deny']='No'
for i in range(0,500):
    x1=res1[i][0]
    x2=res2[i]
    if x2!='No':
        x2=res2[i][0]
    x3=res3[i][1]
    if x2!=x3:
        f2+=1
    if m[x1]!=x3:
        f1+=1
print(str(f1)+' '+str(f2))