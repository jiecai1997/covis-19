import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import requests
import yfinance as yf
from datetime import datetime, timedelta

from data.health import LATEST_DATE

EARLIEST_DATE = datetime.strptime('2020-01-01', '%Y-%m-%d')
DELTA_DAYS = (LATEST_DATE - EARLIEST_DATE).days

BIG_TECH = ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOG', 'MSFT']
INDEXES = ['^DJI', '^GSPC', '^IXIC']

DF = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Stock'])
for t in INDEXES:
    df = yf.download(t, start='2020-01-01', end='2020-04-21').reset_index()
    df['Stock'] = t
    df['% Diff 1D'] = df['Close'].pct_change()
    initial = df[df['Date'] == min(df['Date'])]['Close'][0]
    df['% Diff YTD'] = ((df['Close'] - initial)/initial)*100
    df['Days Since NY'] = df['Date'].apply(lambda x: (x - EARLIEST_DATE).days)
    DF = DF.append(df, ignore_index=True)
