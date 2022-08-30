import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

token_list_url = 'https://www.oklink.com/en/eth/token-list'

token_list_links = pd.DataFrame(columns=['index', 'Token', 'url', 'TX Amount', 'Address Count'])

with webdriver.Chrome(executable_path="C:\webdrivers\chromedriver_103.exe") as driver:
    #open STARTING token list page
    driver.get(token_list_url)
    time.sleep(1)

    #open the dropdown menu at the bottom of the page to select the number of rows to be displayed per page
    row_selection_button = driver.find_element(By.XPATH, '/html/body/div/div/main/div/div[3]/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div')
    row_selection_button.click()
    time.sleep(1)

    #change the number of rows to be displayed to 100 per page from the default of 20
    set_100_row_page = driver.find_element(By.XPATH, '/html/body/div/div/main/div/div[3]/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/div/div/div[4]')
    set_100_row_page.click()
    time.sleep(1)
    #as it is a dynamic webpage grab the new page source and find the number of token pages there are now with 100 rows per page
    token_list_html_source_100_rows = BeautifulSoup(driver.page_source, "html.parser")
    last_token_list_page = token_list_html_source_100_rows.find_all('a', class_='okui-pagination-item-num')
    no_pages_100_rows_per_page = last_token_list_page[-1].text
    
    for page in range(1,int(no_pages_100_rows_per_page)):
        #grab the rows, store in pandas and write to csv
        table = driver.find_element(By.CLASS_NAME, 'rc-table-container')
        rows = table.find_elements(By.TAG_NAME, 'tr')[2:]

        for row in rows:
            row_split = row.find_elements(By.TAG_NAME, 'td')
            row_cleaned = [row_split[0].text, 
                            row_split[1].text,
                            row_split[1].find_element(By.TAG_NAME, 'a').get_attribute('href'),  
                            row_split[4].text,
                            row_split[6].text
                            ]
            token_list_links.loc[len(token_list_links.index)] =  row_cleaned      
            

        #click next page arrow
        
        ul = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[3]/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/ul')
        next_page_button = ul.find_elements(By.TAG_NAME , 'li')[-1]
        next_page_button.click()
        time.sleep(1)
    
    #store the last page
    time.sleep(1)
    table = driver.find_element(By.CLASS_NAME, 'rc-table-container')
    rows = table.find_elements(By.TAG_NAME, 'tr')[2:]

    for row in rows:
        row_split = row.find_elements(By.TAG_NAME, 'td')
        row_cleaned = [row_split[0].text, 
                        row_split[1].text,
                        row_split[1].find_element(By.TAG_NAME, 'a').get_attribute('href'),  
                        row_split[4].text,
                        row_split[6].text
                        ]
        token_list_links.loc[len(token_list_links.index)] =  row_cleaned

    driver.quit()

#print(token_list_links)

token_list_links.to_csv('token_list_links.csv', index=False)