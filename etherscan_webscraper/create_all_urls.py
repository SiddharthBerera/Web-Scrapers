from pprint import pformat
import re
from xml.dom.expatbuilder import parseFragment
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.by import By

url_login='https://etherscan.io/login'

def read_in_url(filename):
    file = open(filename, encoding='UTF8')
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    file.close()
    return rows

def construct_all_urls(rows):
    all_urls=[]
    for row in rows:
        #no_pages_per_label=0
        #start=0
        for i in range(0,3):
            for page_no in range(int(row[i])):
                url = row[i+3][:-17]+str(page_no*100)+'&col=1&order=asc'
                if i==0:
                    all_urls.append([url,'main'])
                elif i==1:
                    all_urls.append([url,'other'])
                elif i==2:
                    all_urls.append([url,'legacy'])
    return all_urls

def write_to_csv(rows, filename):
    f = open(filename, 'w+', encoding='UTF8', newline='')
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
    f.close()

            
base_urls=read_in_url("data\\num_account_urls.csv")
all_urls=construct_all_urls(base_urls)
write_to_csv(all_urls, 'data\\all_urls.csv')