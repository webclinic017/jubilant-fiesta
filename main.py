from datetime import datetime, timedelta
import backtrader as bt
from backtrader.analyzers import PyFolio
from data.data_fetch import fetch_historical_data
from data.custom_pandas_data import CustomPandasData
from strategies.crypto_arbitrage import CryptoArbitrage

# Define the start date for historical data
six_months_ago = (datetime.now() - timedelta(4 * 30)).strftime('%Y-%m-%dT%H:%M:%SZ')

# Fetch historical data
kraken_data = fetch_historical_data('kraken', 'BTC/USD', since=six_months_ago)
coinbase_data = fetch_historical_data('coinbasepro', 'BTC/USD', since=six_months_ago)
bitstamp_data = fetch_historical_data('bitstamp', 'BTC/USD', since=six_months_ago)
# bitfinex_data = fetch_historical_data('bitfinex', 'BTC/USD', since=six_months_ago)


# Create a cerebro instance
cerebro = bt.Cerebro()

# Add analyzers
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
cerebro.addstrategy(CryptoArbitrage)
cerebro.addanalyzer(PyFolio, _name='pyfolio')


# Add data feeds to cerebro
cerebro.adddata(CustomPandasData(dataname=kraken_data, name="Kraken"))
cerebro.adddata(CustomPandasData(dataname=coinbase_data, name="Coinbase"))
cerebro.adddata(CustomPandasData(dataname=bitstamp_data, name="Bitstamp"))
# cerebro.adddata(CustomPandasData(dataname=bitfinex_data, name="Bitfinex"))

# Set initial cash
initial_cash = 100000
cerebro.broker.setcash(initial_cash)


# Run backtest
results = cerebro.run()


performance_report = results[0].analyzers.getbyname('pyfolio')
returns, positions, transactions, gross_lev = performance_report.get_pf_items()
transactions.to_csv('performance_report.csv')


# Get the final value of the portfolio
initial_cash = cerebro.broker.startingcash
final_value = cerebro.broker.getvalue()
profit_loss_percentage = ((final_value - initial_cash) / initial_cash) * 100

print("Initial Cash:", initial_cash)
print("Final Value:", final_value)
print("Profit/Loss Percentage:", profit_loss_percentage, "%")


# Generate a detailed report of the backtest
# plot_args = dict(
#     style='candlestick',
#     barup='green',
#     bardown='red',
#     fmt_x_data='%Y-%m-%d %H:%M',
#     volume=True,
#     title='Crypto HFT Arbitrage Strategy',
#     ylabel='Price',
#     subplot=True
# )
# cerebro.plot(**plot_args)
