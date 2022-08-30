from pprint import pformat
import re
from xml.dom.expatbuilder import parseFragment
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.by import By

#AnonomousSloth Siddharth31!

url_login='https://etherscan.io/login'
url_labels='https://etherscan.io/labelcloud'
account_urls=[]
number_of_account_urls=[]


def sub_string(string, substring):
    i=0
    while i<len(string):
        if string[i:i+len(substring)] == substring:
            return True
        i+=1
    return False
 
def write_account_urls_txt(account_urls, name):
    with open(name, 'w+', encoding='UTF8') as f:
        for url in account_urls:
            f.write(url)
            f.write('\n')   

def write_num_account_urls_csv(num_account_urls, filename):
    f = open(filename, 'w+', encoding='UTF8', newline='')
    writer = csv.writer(f)
    for row in num_account_urls:
        writer.writerow(row)
    f.close()

def other_exists(url_source, name):
    nav_tab = url_source.find("ul", class_="nav nav-custom nav-borderless nav_tabs")
    if nav_tab:
        for item in nav_tab.find_all("li", class_="nav-item"):
            if sub_string(item.text.lower(),name):
                return True
        return False
    else:
        return False

def number_of_pages(url_source):
    pages_container = url_source.find("li", class_="page-item disabled")
    if pages_container:
        page_no_text = pages_container.find_all("strong", class_='font-weight-medium')
        if page_no_text and len(page_no_text)>=2:
            return int(page_no_text[1].text)
    return 1


with webdriver.Chrome(executable_path="C:\webdrivers\chromedriver_103.exe") as driver:
    driver.get(url_login)
    input('please login, complete captcha and press enter upon completion')
    time.sleep(5)

    driver.get(url_labels)
    #time.sleep(5)
    label_word_cloud_source = BeautifulSoup(driver.page_source, "html.parser")
    #collect all the urls to the first page of the label account
    for a in label_word_cloud_source.find_all("a", class_="py-1 px-3 d-block", href=True):
        if sub_string(a['href'].lower(),'/accounts/label'):
            account_urls.append('https://etherscan.io/'+a['href']+'?subcatid=1&size=100&start=0&col=1&order=asc')

    for url in account_urls:
        print(url)
        #starts at main section of labels
        driver.get(url)        
        #print("hi")
        url_source = BeautifulSoup(driver.page_source, "html.parser")
        #checks main page if there is an 'other' or 'legacy' section
        other = other_exists(url_source,'other')
        legacy = other_exists(url_source,'legacy')
        #finds number of pages within main section of label
        no_main_pages = number_of_pages(url_source)
        print(no_main_pages)
        #if there is an 'other' section, finds link to that page and finds number of pages in other section
        if other:
            others_link = driver.find_element(By.PARTIAL_LINK_TEXT,"Others")
            others_link.click()
            url_other_25_page = str(driver.current_url)
            url_other_100_page_other = url_other_25_page+'&size=100&start=0&col=1&order=asc'
            driver.get(url_other_100_page_other)
            url_source = BeautifulSoup(driver.page_source, "html.parser")
            no_other_pages = number_of_pages(url_source)
        else: 
            url_other_100_page_other = ''
            no_other_pages = 0
        #if there is a 'legacy' section, finds link to that page and finds number of pages in other section
        if legacy:
            legacy_link = driver.find_element(By.PARTIAL_LINK_TEXT,"Legacy")
            legacy_link.click()
            url_other_25_page = str(driver.current_url)
            url_other_100_page_legacy = url_other_25_page+'&size=100&start=0&col=1&order=asc'
            driver.get(url_other_100_page_legacy)
            url_source = BeautifulSoup(driver.page_source, "html.parser")
            no_legacy_pages = number_of_pages(url_source)
        else: 
            url_other_100_page_legacy = ''
            no_legacy_pages = 0
        number_of_account_urls.append([str(no_main_pages),str(no_other_pages),str(no_legacy_pages),url,url_other_100_page_other,url_other_100_page_legacy])

        
write_account_urls_txt(account_urls,"data\\account_urls.txt")
write_num_account_urls_csv(number_of_account_urls,"data\\num_account_urls.csv")
