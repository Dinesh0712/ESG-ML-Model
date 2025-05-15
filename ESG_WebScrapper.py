from bs4 import BeautifulSoup
import pandas as pd
import requests
import ipywidgets as widgets
from ipywidgets import interact
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

#check if code is able to access data
try:
    web_data = requests.get('https://sg.finance.yahoo.com/quote/TNVAX/sustainability/').text
    print('Success')
except:
    print('Unable to access URL')


#read file with tickers required
df = pd.read_csv('Ticker_Names.csv') #replace file with nyour own file of tickers

df.head() #check if file can be read

df['Ticker'].value_counts() # check data size
total_ticker = df['Ticker']
print(total_ticker) #check if variable works


#function to obtain ESG scores from yahoo finance
def get_esg_score(ticker): 

    url = "https://finance.yahoo.com/quote/"+ticker+"/sustainability" #ticker is where the values from your file will go to

    # This will reduce bloat or disabel unnecessary stuff so our scraping moves as fast as it can 
    options = Options()
    options.add_argument("--headless=new")  
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false") 
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(10)

    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        h4_tags = soup.find_all('h4')

        # Finds the first numeric h4 value which is usually ESG scores for funds
        for tag in h4_tags:
            text = tag.get_text(strip=True)
            if re.match(r'^\d+(\.\d+)?$', text):
                return float(text)

        return "Not found"

    except:
        return "Not found"

    finally:
        driver.quit()


ESG = []

for ticker in total_ticker:
    try:
        score = get_esg_score(ticker)
        if score:
            ESG.append(score)
        else:
            ESG.append(" ")
    except Exception as e:
        ESG.append(" ")

    # used to check if working. Comment out if just running
    print(ESG) 