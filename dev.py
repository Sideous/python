

import os
os.chdir("C:/Users/John/Documents/python_script")
from array import *
import csv

def llres(r1,r2):
    req=r1*r2
    req=req/(r1+r2)
    return req
    
with open('rs.csv', 'r') as file:
    reader = csv.reader(file)
    i=0
    res=array('f',[0.0])
    synres=array('f',[0.0])
    for each_row in reader:
        res[i]=float(each_row[0])
        res.extend([float(each_row[0])])
        print(res[i], i)
        i=i+1
    file.close()
    k=0
for i in range(len(res)):
    print(i)
    for j in range(len(res)):
        synres[k]=llres(res[i], res[j])
        synres.extend([synres[k]])
        k=k+1
        print(synres[k], k)
        
print("hello", len(res))
