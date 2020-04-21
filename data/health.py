import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from const import COLS_RENAME, STATE_POPULATIONS, US_POPULATION
from app import server

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
        df['Population'] = df['state'].map(STATE_POPULATIONS)
    else:
        df['Population'] = US_POPULATION

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

    # calculate normalized per 100k metrics
    # positive per 100k
    df['Positive per 100k, Cumulative'] = round(df['Positive, Cumulative']/df['Population']*100000, 1)
    df['Positive per 100k, Daily Increase'] = round(df['Positive, Daily Increase']/df['Population']*100000, 1)
    # negative per 100k
    df['Negative per 100k, Cumulative'] = round(df['Negative, Cumulative']/df['Population']*100000, 1)
    df['Negative per 100k, Daily Increase'] = round(df['Negative, Daily Increase']/df['Population']*100000, 1)
    # total tested
    df['Total Tested per 100k, Cumulative'] = round(df['Total Tested, Cumulative']/df['Population']*100000, 1)
    df['Total Tested per 100k, Daily Increase'] = round(df['Total Tested, Daily Increase']/df['Population']*100000, 1)
    # deaths
    df['Deaths per 100k, Cumulative'] = round(df['Deaths, Cumulative']/df['Population']*100000, 1)
    df['Deaths per 100k, Daily Increase'] = round(df['Deaths, Daily Increase']/df['Population']*100000, 1)
    # recovered
    df['Recovered per 100k, Cumulative'] = round(df['Recovered, Cumulative']/df['Population']*100000, 1) 
    # hospitalized
    df['Hospitalized per 100k, Cumulative'] = round(df['Hospitalized, Cumulative']/df['Population']*100000, 1)    
    df['Hospitalized per 100k, Daily Increase'] = round(df['Hospitalized, Daily Increase']/df['Population']*100000, 1)
    # in ICU
    df['In ICU per 100k, Cumulative'] = round(df['In ICU, Cumulative']/df['Population']*100000, 1)    
    df['In ICU per 100k, Currently'] = round(df['In ICU, Currently']/df['Population']*100000, 1)
    # on ventilator
    df['On Ventilator per 100k, Cumulative'] = round(df['On Ventilator, Cumulative']/df['Population']*100000, 1)    
    df['On Ventilator per 100k, Currently'] = round(df['On Ventilator, Currently']/df['Population']*100000, 1)   
    return df

### POST-CALCULATION VARIABLES
# state data
URL_STATES_API = 'https://covidtracking.com/api/v1/states/daily.json'
DF_STATES = dataframe_from_request(URL_STATES_API)
DF_STATES = clean_dataframe(DF_STATES, 'state')

STATES = DF_STATES['State'].unique()

# federal data
URL_FEDERAL_API = 'https://covidtracking.com/api/us/daily'
DF_FEDERAL = dataframe_from_request(URL_FEDERAL_API)
DF_FEDERAL = clean_dataframe(DF_FEDERAL, 'federal')

# date variables
LATEST_DATE = min(max(DF_STATES['date']), max(DF_FEDERAL['date']))
EARLIEST_DATE = max(min(DF_STATES['date']), min(DF_FEDERAL['date']))
DELTA_DAYS = (LATEST_DATE - EARLIEST_DATE).days

