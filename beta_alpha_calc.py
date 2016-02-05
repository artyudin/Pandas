import pandas as pd
import numpy as np
from pandas.io.data import DataReader
from pandas.io import data, wb
import datetime
from datetime import date

class Beta:

	def __init__(self, symbol):

		self.symbol = symbol
		self.start_date = date(2010,12,31)
		self.end_date = date(2013,12,31)
		self.period = 12
		self.stock_returns = self.calculate_stock_returns()
		self.sp_returns = self.calculate_sp_returns()
		
		

	def get_data(self):
		stock = DataReader(self.symbol,'yahoo',self.start_date, self.end_date)
		return stock

	def get_sp_data(self):
		sp = DataReader('^GSPC','yahoo',self.start_date, self.end_date)
		return sp


	def calculate_stock_returns(self):
		stock = self.get_data()
		data = pd.DataFrame({'stock_adj_close':stock['Adj Close']}, index=stock.index)
		data[['stock_returns']] = data[['stock_adj_close']]/data[['stock_adj_close']].shift(1)-1 
		stock_return = data.dropna()
		return stock_return
	
	def calculate_sp_returns(self):
		sp = self.get_sp_data()
		data = pd.DataFrame({'sp_adj_close':sp['Adj Close']}, index=sp.index)
		data[['sp_returns']] = data[['sp_adj_close']]/data[['sp_adj_close']].shift(1)-1 
		sp_return = data.dropna()
		return sp_return


	def compute_covariance(self):
		covariance = np.cov(self.stock_returns['stock_returns'], self.sp_returns['sp_returns'])
		return covariance

	def calculate_beta(self):
		covariance = self.compute_covariance()
		beta = covariance[0,1]/covariance[1,1]
		print('Beta', beta)
		return beta

	def calculate_alpha(self):
		beta = self.calculate_beta()
		alpha = np.mean(self.stock_returns['stock_returns'])-beta*np.mean(self.sp_returns['sp_returns'])
		annualized_alpha = alpha*self.period
		print('annualized_alpha', annualized_alpha)
		return alpha

	def calculate_r_squared(self):
		covariance = self.compute_covariance()
		alpha = self.calculate_alpha()
		beta = self.calculate_beta()
		ypred = alpha+beta*self.sp_returns['sp_returns']
		ss_res = np.sum(np.power(ypred-self.stock_returns['stock_returns'],2))
		ss_tot = covariance[0,0]*(len(self.stock_returns)-1)
		r_squared = 1.-ss_res/ss_tot
		print('r_squared', r_squared)
		return r_squared

	def calculate_volatility(self):
		covariance = self.compute_covariance()
		volatility = np.sqrt(covariance[0,0])
		volatility = volatility*np.sqrt(self.period)
		print('volatility', volatility)

	def calculate_moment(self):
		momentum = np.prod(1+self.stock_returns['stock_returns'].tail(12).values)-1
		print('momentum', momentum)
		return momentum



b = Beta('AAPL')
b.calculate_alpha()
b.calculate_r_squared()
b.calculate_volatility()
b.calculate_moment()




















