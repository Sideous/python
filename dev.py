

import os
os.chdir("C:/Users/John/Documents/python_script")
from array import *
import csv

def llres(r1,r2):
    req=r1*r2
    req=req/(r1+r2)
    return req

def ret_as_float(mystr):
    xx=-10.0
    ss=mystr.split("'")
    if len(ss) < 2:
        return xx
    mystr=ss[1].upper()
    if mystr[len(mystr)-1].isdigit():
        xx=float(mystr)
    elif mystr[len(mystr)-1]=='K':
        ss=mystr.split("K")
        xx=float(ss[0])*1000
    elif mystr[len(mystr)-1]=='M':
        ss=mystr.split("M")
        xx=float(ss[0])*1000000
    elif mystr[len(mystr)-1]=='%':
        ss=mystr.split("%")
        xx=float(ss[0])
    return xx

# Get user input  
print('Enter output voltage as a decimal of the input voltage:')
nx =float(input())
#print ('Output =', nx, ' * input votage')
print ('Enter max value of divider:')
divmax=float(input())
#divmax=ret_as_float(input())
print ('Enter min value of divider:')
divmin=float(input())
#divmin=ret_as_float(input())
#print ('Enter precision needed (0.1%, 1.0% 5.0%):')
#s1=input()
#ss=s1.split("%")
#precis=float(s1[1])


# Build arrays
with open('rs.csv', 'r') as file:
    reader = csv.reader(file)
    i=0
    res=array('f',[0.0])
    synres=array('f',[0.0])
    rvals=[[0,0,0,0," "," "]]
    #Build res[] from values in csv
 #   for each_row in reader:
 #       rvals=rvals+[[float(each_row[0]),1,0,0]]
 #       print(rvals[1+i][0], i)
 #       i=i+1

file.close()

comp_file = open('SMD_RES_0603.ptf', 'r')
i=0
for line in comp_file:
    fields = line.split(" |")
    if i > 7:
        if (len(fields)>2):
            st2=fields[8].split("'")
            if st2[1]=='ACTIVE':
                x=ret_as_float(fields[2])
                st2=fields[11].split("| '")
 #               rvals=rvals+[[x,1,0,0,st2[1]," "]]
                rvals=rvals+[[x,1,0,0," "," "]]
 #               if len(st2) > 1:
 #                   print(fields[0],fields[1],fields[2], x, ret_as_float(fields[5]),fields[8], st2[1])
 #               else:
 #                   print(fields[0],fields[1],fields[2], x, ret_as_float(fields[5]), fields[8])
    i+=1
print(i)    
rvals.pop(0)

    
"""
#Build array of all permitations of parallel combinations
k=len(rvals)-1
for i in range(k):
    for j in range(i,k):
        rvals=rvals+[[llres(rvals[i][0], rvals[j][0]),2,rvals[i][0],rvals[j][0]," "," "]]
        print(rvals[len(rvals)-1][0], j, i)
"""
rvals.sort(reverse=True)
xx=0

import math

#Begin search
factor=1+nx/(1-nx)
z1_max=divmax/factor
z1_min=divmin/factor

print(z1_max, z1_min)
print(divmax,divmin)
last_z1=0
for div_net in range(math.floor(divmax),math.ceil(divmin),-10):
    nx_actual=0   
    z1=0
    num_of_r=0
    z1_target=div_net/(1+nx/(1-nx))                  
    temp_str="{:.2f}, ".format(z1_target) 
    for i in range(len(rvals)):
        if z1 > (0.99 * z1_target):
            break
        elif rvals[i][1] == 1:
            passes= math.floor(z1_target/rvals[i][0])
        else :
            passes=1
        if passes >= 1:
            for j in range(passes):
                if ((z1+rvals[i][0]) < (1.01*z1_target)):
                    z1=z1+rvals[i][0]
                    if rvals[i][1] == 1:
                        temp_str=temp_str + str(rvals[i][0])
                    elif rvals[i][1] == 2:
                        temp_str=temp_str + str(rvals[i][2]) + ",||, " + str(rvals[i][3])
                    temp_str=temp_str + ", "
                    num_of_r=num_of_r+rvals[i][1]
    if (z1 != last_z1) :
        last_z1=z1
    #Find z2
        z2_target=z1*(nx/(1-nx))
        temp_str=temp_str+"{:.3f}, ".format(z2_target)
        z2=0
        for i in range(len(rvals)):
            if z2 > (0.99 * z2_target):
                break
            elif rvals[i][1] == 1:
                passes= math.floor(z2_target/rvals[i][0])
            else :
                passes=1
            if passes >= 1:
                for j in range(passes):
                    if ((z2+rvals[i][0]) < (1.01*z2_target)):
                        z2=z2+rvals[i][0]
                        if rvals[i][1] == 1:
                            temp_str=temp_str + str(rvals[i][0])
                        elif rvals[i][1] == 2:
                            temp_str=temp_str + str(rvals[i][2]) + ",||, " + str(rvals[i][3])
                        temp_str=temp_str + ", "
                        num_of_r=num_of_r+rvals[i][1]
            nx_actual=z2/(z2+z1)            
        temp_str = temp_str + "z1={:.3f}, z2={:.3f}, ".format(z1,z2)
        if (abs(nx_actual-nx) < (.025*nx)) and num_of_r <4:
            print(num_of_r,", {:0.3f}, ".format(nx_actual), temp_str)        
"""
#################################
    temp_str="{:.2f}, ".format(z1_target)
    z1=0
    z2=0
    bestfit_index=-1
    bestfit_delta=1000000
    decimal=z1_target-math.floor(z1_target)
    for i in range(len(rvals)):
        rvals_dec=rvals[1][0]-math.floor(rvals[i][0])
        if (((decimal-rvals_dec) > 0) and ((decimal-rvals_dec) < bestfit_delta)):
            bestfit_delta=decimal-rvals_dec
            bestfit_index=i
    if bestfit_index >= 0: 
        z1=rvals[i][0]
        temp_str=temp_str + "{:0.2f},".format(rvals[i][0])
    for i in range(len(rvals)):
        if z1 > (1.001*z1_target):
            break
        elif rvals[i][1] == 1:
            passes= math.floor(z1_target/rvals[i][0])
        else :
            passes=1
        if passes >= 1:
            for j in range(passes):
                if ((z1+rvals[i][0]) < (1.001*z1_target)):
                    z1=z1+rvals[i][0]
                    if rvals[i][1] == 1:
                        temp_str=temp_str + "{:0.2f},".format(rvals[i][0])
                    elif rvals[i][1] == 2:
                        temp_str=temp_str + "{:0.2f},||, {:0.2f}".format(rvals[i][2],rvals[i][3])
                    temp_str=temp_str + ", "
                    num_of_r=num_of_r+rvals[i][1]

    #Find z2
    z2_target=z1*(nx/(1-nx))
    temp_str=temp_str+"{:.2f}, ".format(z2_target)
    bestfit_index=-1
    bestfit_delta=1000000
    decimal=z2_target-math.floor(z2_target)
    for i in range(len(rvals)):
        rvals_dec=rvals[1][0]-math.floor(rvals[i][0])
        if (((decimal-rvals_dec) > 0) and ((decimal-rvals_dec) < bestfit_delta)):
            bestfit_delta=decimal-rvals_dec
            bestfit_index=i
    if bestfit_index >= 0: 
        z2=rvals[i][0]
        temp_str=temp_str + "{:0.2f},".format(rvals[i][0])
    for i in range(len(rvals)):
        if z2 > (1.001 * z2_target):
            break
        elif rvals[i][1] == 1:
            passes= math.floor(z2_target/rvals[i][0])
        else :
            passes=1
        if passes >= 1:
            for j in range(passes):
                if ((z2+rvals[i][0]) < (1.01*z2_target)):
                    z2=z2+rvals[i][0]
                    if rvals[i][1] == 1:
                        temp_str=temp_str + "{:0.2f},".format(rvals[i][0])
                    elif rvals[i][1] == 2:
                        temp_str=temp_str + "{:0.2f},||, {:0.2f}".format(rvals[i][2],rvals[i][3])
                    temp_str=temp_str + ", "
                    num_of_r=num_of_r+rvals[i][1]
        nx_actual=z2/(z2+z1)            
    temp_str = temp_str + "z1={:.3f}, z2={:.3f}, ".format(z1,z2)
    if (abs(nx_actual-nx) < (.025*nx)) and num_of_r <4:
        print(num_of_r,", {:0.3f}, ".format(nx_actual), temp_str)        

#################################
"""
print("hello", len(res))

