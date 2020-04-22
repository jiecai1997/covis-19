import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import requests
import yfinance as yf
from datetime import datetime, timedelta

from data.health import LATEST_DATE
from const import INDICES, FAANGM, AIRLINES, TICKERS

EARLIEST_DATE = datetime.strptime('2020-01-01', '%Y-%m-%d')
DELTA_DAYS = (LATEST_DATE - EARLIEST_DATE).days

DF = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Stock'])

for t in TICKERS.keys():
    df = yf.download(t, start='2020-01-01').reset_index()
    df['Stock'] = t
    initial = df[df['Date'] == min(df['Date'])]['Close'][0]
    df['$ Delta YTD'] = (df['Close'] - initial)
    df['% Delta YTD'] = ((df['Close'] - initial)/initial)*100
    df['Days Since NY'] = df['Date'].apply(lambda x: (x - EARLIEST_DATE).days)
    df['Company'] = df['Stock'].map(TICKERS)
    df = df.round({'Open': 2, 'High': 2, 'Low':2, 'Close':2, 'Adj Close':2, '$ Delta YTD':2, '% Delta YTD':1})
    DF = DF.append(df, ignore_index=True)
