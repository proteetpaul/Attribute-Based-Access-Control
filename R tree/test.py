import matplotlib.pyplot as plt 
import json

infile=open("plot_arrays.txt","r")
infile2=open("range2.txt","r")
p=json.load(infile)
p2=json.load(infile2)
plt.plot(p[0], p[1], label='R tree')
plt.plot(p[0],p2, label='Seq Search')
plt.xlabel('Range')
plt.ylabel('log of time taken')
plt.legend()
plt.show()

