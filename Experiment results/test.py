import os
import sys
def fun(x):
    x+=1
    if x==5:
        return
    fun(x)
    print(x)
y=0
fun(y)

