# Web-Scrapers
Web Scrapers for Blockchain data aggregator weebsites, to collect different account holder addresses and their associated descriptive label

## Etherscan.com
get_urls.py scrapes the word cloud label section of the website (https://etherscan.io/labelcloud) and returns a csv file (num_account_urls.csv) with all the links for each of the distinct labels in the word label cloud and the number of sub pages under each label. A snippet of this file-
<img width="665" alt="image" src="https://user-images.githubusercontent.com/71666566/187562647-75945fa5-fac6-4c2a-aebe-5e7e83f1cb29.png">

There are potentially thousands of account holders under each label, however etherscan only displays a maximum of 100 addresses in one page, thus
create_all_urls.py then constructs all urls to scrape from and stores them in the csv file all_urls.csv. A snippet of this file-
<img width="660" alt="image" src="https://user-images.githubusercontent.com/71666566/187562802-d742b0d7-4864-4426-b0b3-ae11629b715f.png">

Finally word_cloud_label_scraper.py scrapes the holder addresses and associated labels from each of the constructed links and stores them in the csv file all_accounts_word_label_cloud.csv. A snipet of this file-
<img width="718" alt="image" src="https://user-images.githubusercontent.com/71666566/187563280-fa152faf-b396-4d91-8f23-0eae72c78675.png">


## OKlink.com

