import pandas as pd
import numpy as np
import janitor as jn
import matplotlib.pyplot as plt

def get_timeframe(date_range=('2020-01-01', '2024-12-31')):
    timeframe = pd.DataFrame({
        'Date' : pd.date_range(date_range[0], date_range[1]),
    })
    return timeframe

def get_my_investments(excel_filepath, sheet_name, is_realised = False):
    Investments = pd.read_excel(excel_filepath, sheet_name)
    Investments['Buy date'] = pd.to_datetime(Investments['Buy date'], format="%d-%m-%Y")
    if is_realised:
        Investments['Sell date'] = pd.to_datetime(Investments['Sell date'], format="%d-%m-%Y")
    isin_symbol = pd.read_csv('./EQUITY_L.csv')[["SYMBOL", " ISIN NUMBER"]]

    data = pd.merge(Investments, isin_symbol, left_on='ISIN', right_on=' ISIN NUMBER', how="left")    
    return data


def Unrealised_Investments_daywise(excel_filepath, sheet_name, timeframe):
    investments = get_my_investments(excel_filepath, sheet_name)
    x = (timeframe.conditional_join(investments, ('Date', 'Buy date', '>='))
        .groupby(['Date', 'SYMBOL'], as_index=False)
        .agg({
            'Quantity' : 'sum',
            'Buy value' : 'sum'
        })
    )
    x['Closing price'] = 0.0
    x['Profit'] = 0.0
    x = x[[ "Date", "SYMBOL", 'Quantity', 'Closing price', 'Buy value', 'Profit']]
    return x


def Realised_Investments_daywise(excel_filepath, sheet_name, timeframe):
    investments = get_my_investments(excel_filepath, sheet_name, True)
    x = (timeframe.conditional_join(investments, ('Date', 'Buy date', '>='), 
                                  ('Date', 'Sell date', '<='))
        .groupby(['Date', 'SYMBOL', 'Buy date', 'Sell date'], as_index=False)
        .agg({
            'Quantity' : 'sum',
            'Buy value' : 'sum',
            'Sell value' : 'sum'
        })
    )
    x['Closing price'] = 0.0
    x['Profit'] = np.where(x['Date'] == x['Sell date'], x['Sell value'] - x['Buy value'], 0)
    x = x[[ "Date", "SYMBOL", 'Quantity', 'Closing price', 'Buy value', 'Profit']]
    return x


def get_my_symbols(investments):
    all_symbols = pd.unique(investments['SYMBOL']).tolist()
    all_symbols = [i for i in all_symbols if str(i) != 'nan']
    return all_symbols


def update_closingPrice(investments, symbol_list):
    for symbol in symbol_list:
        symbol_data = pd.read_csv('./New data/{0}.NS.csv'.format(symbol),)[["Date", "Close"]]
        symbol_data['Date'] = pd.to_datetime(symbol_data['Date'], format="%Y-%m-%d",)
        symbol_data['SYMBOL'] = '{0}'.format(symbol)
        
        investments = investments.merge(symbol_data, left_on=['Date', 'SYMBOL'], right_on=["Date", "SYMBOL"], how="left")
        investments = investments.replace(np.nan, 0.0)
        investments.loc[investments['Closing price'] == 0.0, 'Closing price'] = investments['Close']
        investments.drop('Close', axis=1, inplace=True)
    return investments

