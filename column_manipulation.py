import pandas as pd
from pandas import DataFrame
import datetime
from pandas.io import data, wb



def save_csv():

	aapl = pd.io.data.get_data_yahoo('AAPL',
									start=datetime.datetime(2000, 1, 10),
									end=datetime.datetime(2016, 2, 2)
									)

	aapl.to_csv('aapl_price.csv')

save_csv()


def read_csv_file():

	columns = pd.read_csv('aapl_price.csv', index_col='Date', parse_dates=True)
	print(columns.head())

read_csv_file()