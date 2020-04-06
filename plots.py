#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 21:16:19 2020

@author: apolat
"""

import pandas as pd
import matplotlib.pyplot as plt

#Reading data from file  
data=pd.read_csv('data.csv')

#First Plot Under 15 mins adjusted prep time versus Above an Hour
fig = plt.figure()

ax = fig.add_subplot(111)
ax.set_xlim([2.5,5])

data[data['adjusted_prep_time']>=60]['rating'].plot(kind='kde', ax=ax,label='At least an Hour')
data[data['adjusted_prep_time']<=15]['rating'].plot(kind='kde', ax=ax, color='red',label='Under 15 Minutes')
ax.legend(loc='upper left', shadow=True, fontsize=8)

#Second Plot Quick and Easy vs Christmas
urlbook_ids={}
with open('urlbook_ids.csv', 'r') as myfile:
    i = 0
    for row in myfile:
        if i ==  0:
            i += 1
            continue
        splited = row.split(',')
        key = splited[0].strip()[1:-1]
        element = int(splited[1].strip()[1:-1])
        if key in urlbook_ids:
            urlbook_ids[key].append(element)
        else:
            urlbook_ids[key] = [element]

key1='Quick & Easy'
key2='Christmas'
fig = plt.figure()

ax = fig.add_subplot(111)
ax.set_xlim([2.5,5])

data[data['id'].isin(urlbook_ids[key1])]['rating'].plot(kind='kde', ax=ax,label=key1)
data[data['id'].isin(urlbook_ids[key2])]['rating'].plot(kind='kde', ax=ax, color='red',label=key2)
ax.legend(loc='upper left', shadow=True, fontsize=8)

