#!/usr/bin/env python

from os.path import isfile,join,isdir
import numpy as np
import cv2
from PIL import Image
from os import listdir
from os.path import isfile,join,isdir
import os
import time
import shutil
import sys

caliberate_path=os.getcwd()+'/caliberate'
output_path= os.getcwd()+ '/output'
cal_file= os.getcwd()+'/caliberate'+'/cal_values.txt'

class MyException(Exception):
    pass

def chk_file():
    if isdir(caliberate_path):
        if isfile(cal_file):
            ls=[]
            with open(cal_file, "r") as f:
                ls=[tuple(map(int,i.strip().split(' '))) for i in f]
            if(len(ls)==4):
                return ls
            else:
                raise MyException("Please run Caliberate.py|file incompelete")
        else:
            raise MyException("Please run Caliberate.py|file don't exist")
    else:
        raise MyException("Please run Caliberate.py|folder dosen't exist")

def read_output_fold():

    a = Image.open(output_path+'/output.jpg')
    a = a.resize((50,50))
    a = compute_avg_image_color(a)
    return (a)

def compute_avg_image_color(img):
    width,height=img.size

    r_total=0
    g_total=0
    b_total=0
    for x in range(0,width):
        for y in range(0,height):
            r,g,b=img.getpixel((x,y))
            r_total += r
            g_total += g
            b_total += b

    return(r_total,g_total,b_total)

def capture_input_image():
    if (isdir(output_path)):
        shutil.rmtree(output_path)
    os.mkdir(output_path)

    if (isfile(output_path+'output.jpg')):
        os.remove(output_path+'output.jpg')
    time.sleep(1)
    print("taking sample")
    time.sleep(1)
    cam =cv2.VideoCapture(sys.argv[0]) #####video capture######
    s,im=cam.read()
    cv2.imwrite(os.path.join(output_path,'output.jpg'), im)
    cam.release()

compare_value = chk_file() ######           
print("caliberated values:")
print(compare_value)

margin = (10000,10000,10000)
ls_conflicts=[0,0,0,0]
ls_diff=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

while (not[i for i in ls_conflicts if i==1]):
	capture_input_image()
	output_value = read_output_fold()
	for i in range(4):
		if tuple(np.subtract(compare_value[i],margin))<output_value<tuple(np.add(compare_value[i],margin)):
		        ls_conflicts[i] +=1
		        ls_diff[i]=map(abs,list(np.subtract(compare_value[i],output_value)))
	print("output values:")
	print(output_value)        
	print(ls_conflicts)
c=0
for i in ls_conflicts:
    if i>0:
        c+=1
if c>1:
    r_min=sys.maxint
    r_index=-1
    g_min=sys.maxint
    g_index=-1
    b_min=sys.maxint
    b_index=-1
    max_c=[0,0,0,0]
    for i in range(len(ls_diff)):
        if ls_conflicts[i]==1:
            #ls_diff[i]=map(abs,ls_diff[i])
            if ls_diff[i][0]<r_min:
                r_min=ls_diff[i][0]
                r_index=i
            if ls_diff[i][1]<g_min:
                g_min=ls_diff[i][1]
                g_index=i
            if ls_diff[i][2]<b_min:
                b_min=ls_diff[i][2]
                b_index=i
    max_c[r_index]+=1
    max_c[g_index]+=1
    max_c[b_index]+=1    
    for i in range(len(max_c)):
        if max_c[i]>1:
            for j in range(4):
                if i!=j:
                    ls_conflicts[j]=0
    
if ls_conflicts[0]==1:
    print("10 rupees")
if ls_conflicts[1]==1:
    print("100 rupees")    
if ls_conflicts[2]==1:
    print("500 rupees")
if ls_conflicts[3]==1:
    print("2000 rupees")



    			


      
