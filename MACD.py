import talib
import datetime as dt
import pandas_datareader as web
from pandas_datareader import data as pdr
import yfinance as yf


from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG


class MACDStrategy(Strategy):

    def init(self):
        price = self.data.Close
        self.macd = self.I(lambda x: talib.MACD(x)[0], price)
        self.macd_signal = self.I(lambda x: talib.MACD(x)[1], price)

    def next(self):
        if crossover(self.macd, self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal, self.macd):
            self.sell()

start = dt.datetime(2021, 1, 1)
end = dt.datetime(2024, 1, 1)

yf.pdr_override()
data = pdr.get_data_yahoo('TSLA', start, end)

backtest = Backtest(data, MACDStrategy, commission=0.002, exclusive_orders=True)

print(backtest.run())

backtest.plot()