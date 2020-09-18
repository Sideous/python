

import os
os.chdir("C:/Users/John/Documents/python_script")
from array import *
import csv

def llres(r1,r2):
    req=r1*r2
    req=req/(r1+r2)
    return req

#mylist=[[9.0,2]]
#mylist=mylist +[[8.0,1]]
#mylist=mylist+[[11.0,1]]
#mylist.sort(reverse=True)
#print(mylist)
#print(mylist[1])
#print(mylist[1][1])
#print(len(mylist))
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
    rvals=[[0,0,0,0]]
    #Build res[] from values in csv
    for each_row in reader:
        rvals=rvals+[[float(each_row[0]),1,0,0]]
        print(rvals[1+i][0], i)
        i=i+1

file.close()
rvals.pop(0)

    

#Build array of all permitations of parallel combinations
k=len(rvals)-1
for i in range(k):
    for j in range(i,k):
        rvals=rvals+[[llres(rvals[i][0], rvals[j][0]),2,rvals[i][0],rvals[j][0]]]
        print(rvals[len(rvals)-1][0], j)

rvals.sort(reverse=True)
xx=0
size=len(rvals)
for i in range(len(rvals)):
    if (i+1) <= size: 
        if rvals[i][0] == xx:
            print("index",i)
            xx=rvals[i][0]
            xx=rvals.pop(i)
            size=size-1
        
    
import math

#Begin search
factor=1+nx/(1-nx)
z1_max=divmax/factor
z1_min=divmin/factor

print(z1_max, z1_min)

for z1_target in range(math.floor(z1_max),math.floor(z1_min),-1):
    nx_actual=0   
    z1=0
    temp_str=str(z1_target)+ ", "
    for i in range(len(rvals)):
        if z1 > (0.99 * z1_target):
            break
        elif rvals[i][1] == 1:
            passes= math.floor(z1_target/rvals[i][0])
        else :
            passes=1
            print("ok")
        if passes >= 0:
            for j in range(passes):
                z1=z1+rvals[i][0]
                temp_str=temp_str + str(rvals[i][0])
                temp_str=temp_str + ", "
#               print("j=",j ,z1)
    #Find z2
    z2_target=z1*(nx/(1-nx))
    temp_str=str(z2_target)+ ", "
    z2=0
    for i in range(len(rvals)):
        if z2 > (0.99 * z2_target):
            break
        elif rvals[i][1] == 1:
            passes= math.floor(z2_target/rvals[i][0])
        else :
            passes=1
            print("ok")
        if passes >= 0:
            for j in range(passes):
                z2=z2+rvals[i][0]
                if rvals[i][1] == 1:
                    temp_str=temp_str + str(rvals[i][0])
                elif rvals[i][1] == 2:
                    temp_str=temp_str + str(rvals[i][2]) + ",||, " + str(rvals[i][3])
                temp_str=temp_str + ", "
    nx_actual=z2/(z2+z1)            
    temp_str = temp_str + "z1=" + str(z1) +",z2=" +str(z2) +", " + str(nx_actual)
    print(temp_str)
for i in range(len(rvals)):
    xx=rvals[i][0]-math.floor(rvals[i][0])
    if xx > 0:
        print(i, xx)
temp = "start"
temp = temp + ", "
temp = temp + str(synres[0])
print(temp)
#math.floor()
print("hello", len(res))
