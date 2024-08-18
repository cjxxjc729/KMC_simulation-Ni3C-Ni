#!/home/cjx/deepmd-kit-2.2.9/bin/python3.11

import sys


import numpy as np

import os
import time
import re


def regroup_rate_list(rate_list,K_list,step):
 
    #print("rate_list: ")
    #print(len(rate_list))
    #np.savetxt('rate_list.txt',rate_list)
    

    
    if step%5 == 0 and step > 10000:
        for i,rate in enumerate(rate_list):
            #rint("do order 2 fuck!")
            if len(K_list[i]['resutls']) == 2:
                 #print(K_list[i])
                 rate_list[i] = rate_list[i]*1e10

    else:
        weight =  max(rate_list)/2
        rate_list += weight

    #print(K_list)

    #np.savetxt('rate_list.txt',rate_list)
