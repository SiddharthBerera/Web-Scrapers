import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv


url_login='https://etherscan.io/login'

def sub_string(string, substring):
    i=0
    while i<len(string):
        if string[i:i+len(substring)] == substring:
            return True
        i+=1
    return False

def read_in_urls(filename):
    file = open(filename)
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    file.close()
    return rows

"""
In case of 100 per page-
results1 has length of 50 (1,3,...,99)
results2 has length of 50 (2,4,...,100)
sometime there are extra records but we filter for records containing no addresses
"""

def scrape_url(url_to_scrape_from):
    results_page_cleaned=[]
    driver.get(url_to_scrape_from[0])
    if str(driver.current_url) == 'https://etherscan.io/busy':
        time.sleep(10)
        driver.get(url_to_scrape_from[0])

    soup = BeautifulSoup(driver.page_source, "html.parser")
    results_odd = soup.find_all("tr", class_="odd") 
    results_even = soup.find_all("tr", class_="even") 
    results_page = results_odd+results_even
    i=len('https://etherscan.io/accounts/label/')
    j=len(url_to_scrape_from[0])
    while i<len(url_to_scrape_from[0]):
        if url_to_scrape_from[0][i] == '?':
            j=i
            i=len(url_to_scrape_from[0])
        else:
            i+=1
    label=url_to_scrape_from[0][37:j]
            
    for results_row in results_page:
        cells = results_row.find_all("td")
        if sub_string(str(cells[0]),'0x'):
            address = cells[0].text
            name_tag = cells[1].text if len(cells[1]) != 0 else 'N/A'
            balance = cells[2].text[:-6]
            txn_count = cells[3].text
            type = url_to_scrape_from[1]
            results_page_cleaned.append([address,name_tag,balance,txn_count,label,type])
    return results_page_cleaned

def write_to_csv(rows, filename):
    f = open(filename, 'w', newline='', encoding='UTF8')
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
    f.close()

all_urls = read_in_urls("data\\all_urls.csv")
#2281

with webdriver.Chrome(executable_path="C:\webdrivers\chromedriver.exe") as driver:
    driver.get(url_login)
    input('please login, complete captcha and press enter upon completion')
    
    rows=[]
    for url in all_urls:
        rows += scrape_url(url)
        print(url)  

write_to_csv(rows,'data\\all_accounts_word_label_cloud.csv')
