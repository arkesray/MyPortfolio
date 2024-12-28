from extract_history import *
from main import *


config = {
    "generate_history_symbol" : ["none", "required", "all"][0],
    "rpt_prefix" : ["","Personal/"][0]
}

def main():
    timeframe = get_timeframe(('2020-01-01', '2024-12-30'))

    my_unrealised_investments = Unrealised_Investments_daywise(f'./{config["rpt_prefix"]}rpt.xlsx', 'Unrealised', timeframe)
    my_realised_investments = Realised_Investments_daywise(f'./{config["rpt_prefix"]}rpt.xlsx', 'Realised', timeframe)

    my_total_investments = pd.concat([my_unrealised_investments, my_realised_investments])
    my_symbols = get_my_symbols(my_total_investments)

    if config['generate_history_symbol'] == "none":
        pass
    elif config['generate_history_symbol'] == "all":
        get_stock_history(get_all_symbol())
    elif config['generate_history_symbol'] == "required":
        get_stock_history( sorted([f'{i}.NS' for i in my_symbols]) )

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

    plt.plot(portfolio['Date'], portfolio['Current value'], color="red")
    plt.plot(portfolio['Date'], portfolio['Buy value'], linestyle="--", color="blue")
    plt.plot(portfolio['Date'], portfolio['Cum Profit'], color="green")
    plt.show()

if __name__ == "__main__":
    main()
