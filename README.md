# All recipes scraping

A Simple web scrapping project for allrecepies.com

## scraping.py

This file collects recipe categories and store recipe webpages for each category. Then using recipe webpages creates a data file containing average rating, prep time and serving size. An additional adjusted prep time variable is created which is basically prep time per serving.

## plotting.py

This file creates plots comparing the distribution of average ratings for custom categories based on adjusted prep time and original categories of the allrecipes.com website.