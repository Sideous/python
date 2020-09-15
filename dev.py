

import os
os.chdir("C:/Users/John/Documents/python_script")
from array import *
import csv

def llres(r1,r2):
    req=r1*r2
    req=req/(r1+r2)
    return req
    

# Get user input  
print('Enter output voltage as a decimal of the input voltage:')
nx =float(input())
#print ('Output =', nx, ' * input votage')
print ('Enter max value of divider:')
divmax=float(input())
print ('Enter min value of divider:')
divmin=float(input())

# Build arrays
with open('rs.csv', 'r') as file:
    reader = csv.reader(file)
    i=0
    res=array('f',[0.0])
    synres=array('f',[0.0])
    #Build res[] from values in csv
    for each_row in reader:
        res[i]=float(each_row[0])
        res.extend([float(each_row[0])])
        print(res[i], i)
        i=i+1

file.close()
#res.sort()
res.pop(i)
    
k=0
#Build array of all permitations of parallel combinations
for i in range(len(res)):
    for j in range(len(res)):
        synres[k]=llres(res[i], res[j])
        synres.extend([synres[k]])
        k=k+1
        print(synres[k], k)

import math

#Begin search
factor=1+nx/(1-nx)
z1_max=divmax/factor
z1_min=divmin/factor



for z1_target in range(math.floor(z1_max),math.floor(z1_min),-1):
    z1=0
    temp_str=""
    for i in range(len(res)):
        if z1 > (0.99 * z1_target):
            break
        passes= math.floor(z1_target/res[i])-1
        if passes >= 0:
            for j in range(passes):
                z1=z1+res[i]
                temp_str=temp_str + str(res[i])
                temp_str=temp_str + ", "
                print("j=",j)
    print(temp_str)
        
    
temp = "start"
temp = temp + ", "
temp = temp + str(synres[0])
print(temp)
#math.floor()
print("hello", len(res))
