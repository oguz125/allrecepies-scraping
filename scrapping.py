#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 11:07:16 2020

@author: apolat

Scraping allrecipes.com recipe pages for ratings and prep time
"""
import requests
import time
import csv
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def get_url_data(url, max_tries=3):
    remaining_tries = max_tries
    while remaining_tries > 0:
        try:
            return requests.get(url)
        except:
            time.sleep(10)
        remaining_tries = remaining_tries - 1
    return None

url='https://www.allrecipes.com/recipes/'
page=get_url_data(url)
soup = BeautifulSoup(page.content, 'html.parser')

#First we get the categories for the recipes
categories={}
for item in soup.findAll('div', {'class': 'all-categories-col'}):
    for category in item.findAll('li'):
        categories[category.text]=category.a['href']
        

#Then we collect all recipe pages for each category
urlbook={}

for key in categories.keys():
    urlbook[key]=[]
    for i in range(30):
        url=categories[key]+'/?page='+str(i)
        page=get_url_data(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        url_list=soup.findAll('div', {'class': 'grid-card-image-container'})
        for a in url_list:
            urlbook[key].append(a.a['href'])

#Saving the webpages for each category to the file
with open('categories_and_links.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['category', 'link'])
    for key, rows in urlbook.items():
        for row in rows:
            wr.writerow([key, row])

''' 
#To read from file to access the urlbook dictionary use this:
urlbook={}

with open('categories_and_links.csv', 'r') as myfile:
    i = 0
    for row in myfile:
        if i ==  0:
            i += 1
            continue
        splited = row.split(',')
        key = splited[0].strip()[1:-1]
        element = splited[1].strip()[1:-1]
        if key in urlbook:
            urlbook[key].append(element)
        else:
            urlbook[key] = [element]
'''

#Storing id & category pairs for future use
urlbook_ids=dict.fromkeys(urlbook.keys())
for key in urlbook.keys():
    urlbook_ids[key]=[]
    for item in urlbook[key]:
        try:
            id_=int(item.split('/')[4])
        except:
            continue
        urlbook_ids[key].append(id_)

with open('urlbook_ids.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['category', 'id'])
    for key, rows in urlbook_ids.items():
        for row in rows:
            wr.writerow([key, row])
            
#Main data generating step       

data={'id':[],'rating':[],'prep_time':[],'serving':[]}
data=pd.DataFrame(data=data)
failed = []

for key, rows in urlbook.items():
    iteri=0
    data={'id':[],'rating':[],'prep_time':[],'serving':[]}
    data=pd.DataFrame(data=data)
    failed = []
    for row in rows:
        try:
            iteri += 1
            if iteri%10==0:
                print(".")
            id_=int(row.split('/')[4])
            if id_ in data['id']:
                continue
            page=get_url_data(row)
            if page is None:
                failed.append(row)
                print("This page failed %s" % row)
                continue
            soup=BeautifulSoup(page.content, 'html.parser')
            
            if soup.find('div',{'class':'rating-stars'}) is not None:
                try:
                    rating=float(soup.find('div',{'class':'rating-stars'})['data-ratingstars'])
                except:
                    continue
            elif soup.find('div',{'class':'component recipe-reviews container-full-width template-two-col with-sidebar-right main-reviews'}) is not None:
                try:
                    rating=float(soup.find('div',{'class':'component recipe-reviews container-full-width template-two-col with-sidebar-right main-reviews'})['data-ratings-average'])
                except:
                    continue
            else:
                continue
            
            if soup.find('span',{'class':'ready-in-time'}) is not None:
                try:
                    prep_time=soup.find('span',{'class':'ready-in-time'}).text
                except:
                    continue
            elif soup.findAll('div',{'class':'two-subcol-content-wrapper'}) is not None:
                try:
                    prep_time=soup.findAll('div',{'class':'two-subcol-content-wrapper'})[0].findAll('div',{'class':'recipe-meta-item'})[2].find('div',{'class':'recipe-meta-item-body'}).text.replace('\n','').strip()
                except:
                    continue
            else:
                continue
            try:
                prep_time=prep_time.split(' ')
            except:
                continue
            if len(prep_time)==4:
                prep_time=60*int(prep_time[0])+int(prep_time[2])
            elif prep_time[1]=='h':
                prep_time=int(prep_time[0])*60
            else:
                prep_time=int(prep_time[0])
            if soup.find('meta',{'id':'metaRecipeServings'}) is not None:
                serving=int(soup.find('meta',{'id':'metaRecipeServings'})['content'])
            elif soup.findAll('div',{'class':'two-subcol-content-wrapper'}) is not None:
                serving=int(soup.findAll('div',{'class':'two-subcol-content-wrapper'})[1].findAll('div',{'class':'recipe-meta-item'})[0].find('div',{'class':'recipe-meta-item-body'}).text.replace('\n','').strip())
            else:
                continue
            data=data.append({'id':id_,'rating':rating,'prep_time':prep_time,'serving':serving} , ignore_index=True)
            if iteri%500==0:
                print("%f percent is done. Current data length is %d." %(iteri/500,len(data)))
        except Exception as e:
            print("something went wrong %s" % str(e))
            failed.append(row)
            continue
    print("Key %s is done" % key)

data=data.drop_duplicates(subset='id')
data=data[data['prep_time']>1.0]
data['adjusted_prep_time']=data['prep_time']/data['serving']

#Saving data to the file
data.to_csv('data.csv',index=False)



