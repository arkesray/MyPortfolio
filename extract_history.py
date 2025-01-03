import pandas as pd
import time
import multiprocessing
from selenium import webdriver
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime
from pathlib import Path

from config import save_path

def get_all_symbol():
    isin_symbols = pd.read_csv('./EQUITY_L.csv')
    return sorted([f'{i}.NS' for i in isin_symbols['SYMBOL'].values.tolist()])


# print(get_all_symbol())

def get_stock_history(symbol, save_path=save_path, 
                        epoch_start=datetime(2000,1,1).timestamp(), epoch_end= datetime.now().timestamp()
                        ):
    Path(save_path).mkdir(parents=True, exist_ok=True)
    url = f"https://finance.yahoo.com/quote/{symbol}/history/?period1={epoch_start}&period2={epoch_end}"

    options = webdriver.ChromeOptions()
    options.add_argument("log-level=3")
    options.add_argument("headless")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    html=driver.page_source
    driver.quit()
    soup=BeautifulSoup(html,'html.parser')
    html_table=soup.find("table", {"class":"table yf-j5d1ld noDl"} )
    table=pd.read_html(StringIO(str(html_table)))
    data_df = table[0][['Date', 'Open', 'High', 'Low', 'Close Close price adjusted for splits.']]
    data_df = data_df.rename(columns={'Close Close price adjusted for splits.' : 'Close'})
    
    # data_df.loc[:,'Date'] = pd.to_datetime(data_df['Date'], format="%b %d, %Y")
    data_df['Date'] = pd.to_datetime(data_df['Date'], format="%b %d, %Y")
    
    cols = ['Open', 'High', 'Low', 'Close']
    data_df[cols] = data_df[cols].apply(pd.to_numeric, errors='coerce')
    data_df = data_df.dropna()
    
    data_df.to_csv(f'{save_path}/{symbol}.csv', index=False)
    print(f'Created csv file for {symbol}')


def get_stock_history_parallel(symbol_list, save_path=save_path, 
                        epoch_start=datetime(2000,1,1).timestamp(), epoch_end= datetime.now().timestamp()
                        ):
    Path(save_path).mkdir(parents=True, exist_ok=True)
    
    pool = multiprocessing.Pool() 
    pool = multiprocessing.Pool(processes=8) 
    pool.map(get_stock_history, symbol_list) 

    




def main():
    s = ['INFY', 'TCS', 'TATAMOTORS']
    s = [f'{i}.NS' for i in s]
    # s = get_all_symbol()
    get_stock_history_parallel(s)




if __name__ == "__main__":
    main()
