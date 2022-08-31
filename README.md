# Web-Scrapers
Web Scrapers for Blockchain data aggregator weebsites, to collect different account holder addresses and their associated descriptive label

## Etherscan.com
Etherscan is an on chain data aggregator for the ethereum blockchain. It contains a section called the word cloud label where they have managed to give some of the holder addresses a descriptive name, the goal of this bot is to collect all these holder addresses and their label where it exists.
One of the biggest issues initally faced was that a login and v2 recaptcha was required to be completed in order to access the data. Furthermore the website contains v3 recaptchas that check for bot activity. The solution to first issue was using selenium to allow the user to take over when a login or v2 recaptcha (select the relevant images to prove you are not a bot) was met. The second issue was resolved by monitoring the website resources being used and having the bot stop when it exceeded certain levels.

get_urls.py scrapes the word cloud label section of the website (https://etherscan.io/labelcloud) and returns a csv file (num_account_urls.csv) with all the links for each of the distinct labels in the word label cloud and the number of sub pages under each label. A snippet of this file-
<img width="665" alt="image" src="https://user-images.githubusercontent.com/71666566/187562647-75945fa5-fac6-4c2a-aebe-5e7e83f1cb29.png">

There are potentially thousands of account holders under each label, however etherscan only displays a maximum of 100 addresses in one page, thus
create_all_urls.py then constructs all urls to scrape from and stores them in the csv file all_urls.csv. A snippet of this file-
<img width="660" alt="image" src="https://user-images.githubusercontent.com/71666566/187562802-d742b0d7-4864-4426-b0b3-ae11629b715f.png">

Finally word_cloud_label_scraper.py scrapes the holder addresses and associated labels from each of the constructed links and stores them in the csv file all_accounts_word_label_cloud.csv. A snipet of this file-
<img width="718" alt="image" src="https://user-images.githubusercontent.com/71666566/187563280-fa152faf-b396-4d91-8f23-0eae72c78675.png">


## OKlink.com
OKlink is another website that aggregates on chain data for the ethereum blockchain. The Token List section of the website contains over 3000 of the top tokens by market cap and the associated top 10000 holders for each of these tokens along with a descriptive label for some of these addresses. 
The again goal was to scrape these labels.
For this bot I improved my implementation of the previously implemented etherscan bot by keeping the same solution to the recaptchas issue. 
However, I noticed the website would load data by using an internal API which required an API key but the key was unencrypted and so could be copied by reading the requests sent by the page-
<img width="697" alt="image" src="https://user-images.githubusercontent.com/71666566/187565519-8d2e0fb0-fde5-4240-9cc9-fa8cc49c6db4.png">

The bot uses selenium to click a certain button on the webpage that queries this API-
<img width="728" alt="image" src="https://user-images.githubusercontent.com/71666566/187565650-ad74c298-1c03-48eb-a6f9-0fe236dba162.png">

then reads the latest request from this page and stores this API key to then query the internal API directly. When this key expires the bot repeats the process of clicking the webpage to create a request and then read the associated API key, this is required as the API has a limit of 150 rows and around 36 million rows need to be read.
