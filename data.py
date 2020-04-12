import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

### METHODS
def dataframe_from_request(url):
    '''
    Returns pandas dataframe from API request's JSON format

    Args:
        url (string): URL to get API request in JSON format
    Returns:
        df (pandas dataframe): Data in clean panda dataframe format
    '''

    r = requests.get(url)
    if (r.ok):
        data = r.json()
        df = pd.json_normalize(data)

    return df

def clean_dataframe(df):
    '''
    Cleans dataframe:
        - convert date column to datetime type
        -  fill in missing values

    Args:
        df (pandas dataframe): original dataframe
    Returns:
        df (pandas dataframe): cleaned dataframe
    '''

    # datetime date column
    df['date'] = pd.to_datetime(df['date'].apply(str), format='%Y%m%d')

    # string date column
    df['dateString'] = df['date'].dt.strftime('%Y-%m-%d')

    # number of days since 1st case in US
    EARLIEST_DATE = min(df['date'])
    df['daysSinceCase1'] = df['date'].apply(lambda x: (x - EARLIEST_DATE).days)

    # fill NAs
    df.fillna(0, inplace=True)

    return df

### VARIABLES
# metadata
URL = "https://covidtracking.com/api/v1/states/daily.json"
DF = dataframe_from_request(URL)
DF = clean_dataframe(DF)

# date variables
LATEST_DATE = max(DF['date'])
EARLIEST_DATE = min(DF['date'])
DELTA_DAYS = (LATEST_DATE - EARLIEST_DATE).days

# misc variables
NEWLINE = '\n'