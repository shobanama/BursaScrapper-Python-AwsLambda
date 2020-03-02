#LIBRARIES
import requests
import urllib.request
import time
import pandas as pd
import boto3
from bs4 import BeautifulSoup
import datetime


def setup():
  #PREPARE DF
  shariah = pd.DataFrame()

  #LOOP FETCH URL
  for i in range(1, 20):
    url = 'https://www.bursamalaysia.com/market_information/shariah_compliant_equities_prices?per_page=50&page='+str(i)
    response = requests.get(url)
      
  #BS ELEMENT
    soup = BeautifulSoup(response.text, "html.parser")
    data = []
    table = soup.find('table', attrs={'class':'table datatable-striped text-center equity_prices_table datatable-with-sneak-peek js-anchor-price-table'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
      
  #APPEND DF
    df = pd.DataFrame(data)
    df2 = df.iloc[:, :-1]
    shariah = shariah.append(df2, ignore_index = True)
    
  #RENAME COLUMNS
    shariah_table = shariah.rename(columns = {0: "NO", 1: "NAME", 2: "CODE", 3: "REM", 4: "LAST_DONE", 5: "LACP", 6: "CHG", 7: "%CHG", 8: "VOL('00)", 9: "BUY_VOL('00)", 10: "BUY", 11: "SELL", 12: "SEL_VOL('00)", 13: "HIGH", 14: "LOW"})

  #SAVING FILE
    current_date = time.strftime("%Y%m%d")
    shariah_table.to_csv(current_date + "_shariah_fulldump.csv")

  return datetime.datetime.now()
