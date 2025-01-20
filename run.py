from extract_history import *
from main import *
from config import *


def main():
    timeframe = get_timeframe((START_DATE, END_DATE))

    my_unrealised_investments = Unrealised_Investments_daywise(f'./{REPORT_PREFIX}rpt.xlsx', 'Unrealised', timeframe)
    my_realised_investments = Realised_Investments_daywise(f'./{REPORT_PREFIX}rpt.xlsx', 'Realised', timeframe)

    my_total_investments = pd.concat([my_unrealised_investments, my_realised_investments])
    my_symbols = get_my_symbols(my_total_investments)

    if GENERATE_STOCK_HISTORY == 1:
        get_stock_history_parallel( sorted([f'{i}.NS' for i in my_symbols]) )
    elif GENERATE_STOCK_HISTORY == 2:
        get_stock_history_parallel(get_all_symbol())
    else:
        print("Skipping Stock history generation..")


    my_investments_updated = update_closingPrice(my_total_investments, my_symbols)
    my_investments_updated['Current value'] = my_investments_updated['Quantity'] * my_investments_updated['Closing price']
    
    # print(my_investments_updated)
    # my_investments_updated.to_csv('my_investments.csv')

    portfolio = my_investments_updated.groupby(['Date'], as_index=False).agg({
        'Buy value' : 'sum',
        'Current value' : 'sum',
        'Profit' : 'sum',
    })

    portfolio['Cum Profit'] = portfolio['Profit'].cumsum()
    portfolio = portfolio[portfolio['Current value'] != 0]
    
    plt.plot(portfolio['Date'], portfolio['Current value'], color="salmon", label="Current Value")
    plt.plot(portfolio['Date'], portfolio['Buy value'], linestyle="--", color="cornflowerblue", label="Investment Value")
    plt.plot(portfolio['Date'], portfolio['Cum Profit'], color="limegreen", label="Cumulative Realised Profit")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
