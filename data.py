import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from const import COLS_RENAME#, COLS_REORDER

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

def clean_dataframe(df, level):
    '''
    Cleans dataframe:
        - create columns for date variables in datettime and string format 
        - calclates days since first US case
        - fill in missing values
        - rename columns to human readabl format
        - reorder columns for display

    Args:
        df (pandas dataframe): original dataframe
    Returns:
        df (pandas dataframe): cleaned dataframe
    '''

    if level == 'state':
        # remove US territories for 50 states + DC info only
        df = df[~df['state'].isin(['AS', 'GU', 'MP', 'PR', 'VI'])]

    # datetime date column
    df['date'] = pd.to_datetime(df['date'].apply(str), format='%Y%m%d')

    # string date column
    df['Date'] = df['date'].dt.strftime('%Y-%m-%d')

    # number of days since 1st case in US
    EARLIEST_DATE = min(df['date'])
    df['Days Since First Case'] = df['date'].apply(lambda x: (x - EARLIEST_DATE).days)

    # fill NAs
    df.fillna(0, inplace=True)

    # rename columns to human readable format
    df.rename(columns=COLS_RENAME, inplace=True)
    if level == 'state':
        df.rename(columns={'state': 'State',}, inplace=True)

    # reorder columns for display
    #df = df[COLS_REORDER]

    return df

### POST-CALCULATION VARIABLES
# state data
URL_STATES_API = 'https://covidtracking.com/api/v1/states/daily.json'
DF_STATES = dataframe_from_request(URL_STATES_API)
DF_STATES = clean_dataframe(DF_STATES, 'state')

# federal data
URL_FEDERAL_API = 'https://covidtracking.com/api/us/daily'
DF_FEDERAL = dataframe_from_request(URL_FEDERAL_API)
DF_FEDERAL = clean_dataframe(DF_FEDERAL, 'federal')

# date variables
LATEST_DATE = min(max(DF_STATES['date']), max(DF_FEDERAL['date']))
EARLIEST_DATE = max(min(DF_STATES['date']), min(DF_FEDERAL['date']))
DELTA_DAYS = (LATEST_DATE - EARLIEST_DATE).days

