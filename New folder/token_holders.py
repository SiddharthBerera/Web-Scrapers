from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import requests 

import csv
import json
from requests.structures import CaseInsensitiveDict
import pandas as pd
import re

import time

T = time.time()
page_urls = pd.read_csv("token_list_links.csv", usecols = ['url']).squeeze()
page_urls = page_urls.array

with open('holder_tags.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    header = ['holderAddress', 'tokenContractAddress', 'value', 'transactionCount', 'firstTransferTime', 'lastTransferTime', 'totalSend', 'totalReceive', 'sendCount', 'receiveCount', 'legalRateEth', 'ethValue', 'percentChange24h', 'rate', 'precision', 'rank', 'isContract', 'hover', 'tag', 'legalRate']
    writer.writerow(header)
    f.close()

def get_api_key(driver, page_url, api_base_url):
    menu_dropdown = driver.find_element(By.XPATH, '/html/body/div/div/div/div[5]/div/div[3]/div[1]/div/div')
    menu_dropdown.click()
    time.sleep(5)
    button = driver.find_element(By.XPATH, '/html/body/div/div/div/div[5]/div/div[3]/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]')
    button.click()
    for request in driver.requests:
        if request.headers['referer'] == page_url and api_base_url in request.url:
            api_key = request.headers['x-apikey']
            return api_key

def request_url(address, offset, limit):
    t = str(int(round(time.time() * 1000)))
    #https://www.oklink.com/api/explorer/v2/eth/tokens/holders/0xdac17f958d2ee523a2206206994597c13d831ec7?t=1660174950256&chain=eth&tokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&explorerName=ETH&limit=20&offset=0&isSm=true&start=&end=
    #'https://www.oklink.com/api/explorer/v2/eth/tokens/holders/' + address + '?t=' + t + '&chain=eth' + '&tokenAddress=' + address + '&explorerName=ETH' + '&limit=' + limit + '&offset=' + offset + '&isSm=true&start=&end=
    url = 'https://www.oklink.com/api/explorer/v2/eth/tokens/holders/'+address+'?t='+t+'&chain=eth'+'&tokenAddress='+address+'&explorerName=ETH'+ '&limit='+str(limit) + '&offset='+str(offset)
    return url

def query_api(api_key, api_url):
    headers = CaseInsensitiveDict()
    headers["x-apikey"] = api_key
    headers["x-cdn"] = "https://static.oklink.com"
    response = requests.get(api_url, headers=headers)
    msg = json.loads(response.content.decode('utf-8'))
    return msg


LIMIT = 150
FIRST_PAGE_URL = 'https://www.oklink.com/en/eth/token/0xdac17f958d2ee523a2206206994597c13d831ec7'
FIRST_PAGE_API_URL = 'https://www.oklink.com/api/explorer/v2/eth/tokens/holders/0xdac17f958d2ee523a2206206994597c13d831ec7'


with webdriver.Chrome(executable_path="C:\webdrivers\chromedriver_103.exe") as driver:

    driver.get(FIRST_PAGE_URL)
    time.sleep(5)
    api_key = get_api_key(driver, FIRST_PAGE_URL, FIRST_PAGE_API_URL)

    for token in page_urls:
        i=0
        print(time.time()-T)
        offset = 0
        address = re.search(r'\b0x\w+', token).group()
        continue_query = True

        api_url = request_url(address, offset, LIMIT)

        #loops until no more data to gather
        while continue_query:
            print(api_url)    
            msg = query_api(api_key, api_url)
            msg_code = msg['code']
            i+=1
            print(i)

            #contains data
            if msg_code == 0:
                if msg['data']['total'] == 0:
                    continue_query = False
                else:
                    #get data
                    data = msg['data']['hits']
                    df = pd.DataFrame(data)
                    df.to_csv('data.csv', mode='a', index=False, header=False)
                    #update url and offset
                    api_url = api_url.replace('offset='+str(offset), 'offset='+str(offset+LIMIT))
                    offset+=LIMIT

            #eror - incorrect api key
            #update key
            elif msg_code == 5005:
                print('it happened bro')
                api_key = get_api_key(driver, FIRST_PAGE_URL, FIRST_PAGE_API_URL) 
                api_url = request_url(address, offset, LIMIT)
                
            #error - over offset
            #stop searching
            elif msg_code == 4103:
                continue_query = False

            
            