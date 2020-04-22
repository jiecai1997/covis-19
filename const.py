### CONSTANT VARIABLES

# stock tickers
INDEXES = {
    '^IXIC': 'NASDAQ',
    '^GSPC': 'S&P 500',
    '^DJI': 'Dow Jones'
}
FAANGM = {
    'FB': 'Facebook',
    'AAPL': 'Apple',
    'AMZN': 'Amazon',
    'NFLX': 'Netflix',
    'GOOG': 'Google',
    'MSFT': 'Microsoft'
}

TICKERS = {**INDEXES, **FAANGM}

# renaming columns in df
COLS_RENAME = {
    # positive
    'positive': 'Positive, Cumulative',
    'positiveIncrease': 'Positive, Daily Increase',
    # negative
    'negative': 'Negative, Cumulative',
    'negativeIncrease': 'Negative, Daily Increase',
    # total tested (positive + negative)
    'totalTestResults': 'Total Tested, Cumulative',
    'totalTestResultsIncrease': 'Total Tested, Daily Increase',
    # death
    'death': 'Deaths, Cumulative',
    'deathIncrease': 'Deaths, Daily Increase',
    # recovered
    'recovered': 'Recovered, Cumulative',
    # hospitalized
    'hospitalized': 'Hospitalized, Cumulative',
    'hospitalizedIncrease': 'Hospitalized, Daily Increase',
    # in ICU - cumulative and current are swapped in tracker API
    'inIcuCumulative': 'In ICU, Currently',
    'inIcuCurrently': 'In ICU, Cumulative',
    # on ventilator - cumulative and current are swapped in tracker API
    'onVentilatorCumulative': 'On Ventilator, Currently',
    'onVentilatorCurrently': 'On Ventilator, Cumulative',
}
COLS_REORDER = ['Date'] + list(COLS_RENAME.values()) + ['date', 'Days Since First Case']

# metric select options
METRIC_SELECT_OPTIONS = [
    # positive
    {'label': 'Positive, Cumulative', 'value': 'Positive, Cumulative'},
    {'label': 'Positive, Daily Increase', 'value': 'Positive, Daily Increase'},
    # positive per 100k
    {'label': 'Positive per 100k, Cumulative', 'value': 'Positive per 100k, Cumulative'},
    {'label': 'Positive per 100k, Daily Increase', 'value': 'Positive per 100k, Daily Increase'},
    # negative
    {'label': 'Negative, Cumulative', 'value': 'Negative, Cumulative'},
    {'label': 'Negative, Daily Increase', 'value': 'Negative, Daily Increase'},
    # negative per 100k
    {'label': 'Negative per 100k, Cumulative', 'value': 'Negative per 100k, Cumulative'},
    {'label': 'Negative per 100k, Daily Increase', 'value': 'Negative per 100k, Daily Increase'},
    # total tested (positive + negative)
    {'label': 'Total Tested, Cumulative', 'value': 'Total Tested, Cumulative'},
    {'label': 'Total Tested, Daily Increase', 'value': 'Total Tested, Daily Increase'},
    # total tested (positive + negative) per 100k
    {'label': 'Total Tested per 100k, Cumulative', 'value': 'Total Tested per 100k, Cumulative'},
    {'label': 'Total Tested per 100k, Daily Increase', 'value': 'Total Tested per 100k, Daily Increase'},
    # deaths
    {'label': 'Deaths, Cumulative', 'value': 'Deaths, Cumulative'},
    {'label': 'Deaths, Daily Increase', 'value': 'Deaths, Daily Increase'},
    # deaths per 100k
    {'label': 'Deaths per 100k, Cumulative', 'value': 'Deaths per 100k, Cumulative'},
    {'label': 'Deaths per 100k, Daily Increase', 'value': 'Deaths per 100k, Daily Increase'},
    # recovered
    {'label': 'Recovered, Cumulative', 'value': 'Recovered, Cumulative'},
    # recovered per 100k
    {'label': 'Recovered per 100k, Cumulative', 'value': 'Recovered per 100k, Cumulative'},
    # hospitalized
    {'label': 'Hospitalized, Cumulative', 'value': 'Hospitalized, Cumulative'},
    {'label': 'Hospitalized, Daily Increase', 'value': 'Hospitalized, Daily Increase'},
    # hospitalized per 100k
    {'label': 'Hospitalized per 100k, Cumulative', 'value': 'Hospitalized per 100k, Cumulative'},
    {'label': 'Hospitalized per 100k, Daily Increase', 'value': 'Hospitalized per 100k, Daily Increase'}, 
    # in ICU
    {'label': 'In ICU, Cumulative', 'value': 'In ICU, Cumulative'},
    {'label': 'In ICU, Currently', 'value': 'In ICU, Currently'},
    # in ICU per 100k
    {'label': 'In ICU per 100k, Cumulative', 'value': 'In ICU per 100k, Cumulative'},
    {'label': 'In ICU per 100k, Currently', 'value': 'In ICU per 100k, Currently'},
    # on ventilators
    {'label': 'On Ventilator, Cumulative', 'value': 'On Ventilator, Cumulative'},
    {'label': 'On Ventilator, Currently', 'value': 'On Ventilator, Currently'},
    # on ventilators per 100k
    {'label': 'On Ventilator per 100k, Cumulative', 'value': 'On Ventilator per 100k, Cumulative'},
    {'label': 'On Ventilator per 100k, Currently', 'value': 'On Ventilator per 100k, Currently'}
]

# metric definitions, source: https://covidtracking.com/api
METRIC_DEFINITIONS = {
    # positive
    'Positive, Cumulative': 'Total cumulative positive test results.',
    'Positive, Daily Increase': 'Positive test results increase from the day before.',
    # positive per 100k
    'Positive per 100k, Cumulative': 'Total cumulative positive test results, normalized rate to per 100k population.',
    'Positive per 100k, Daily Increase': 'Positive test results increase from the day before, normalized rate to per 100k population.',
    # negative
    'Negative, Cumulative': 'Total cumulative negative test results.',
    'Negative, Daily Increase': 'Negative test results increase from the day before.',
    # negative per 100k
    'Negative per 100k, Cumulative': 'Total cumulative negative test results, normalized rate to per 100k population.',
    'Negative per 100k, Daily Increase': 'Negative test results increase from the day before, normalized rate to per 100k population.',
    # total tested 
    'Total Tested, Cumulative': 'Total cumulative test results (positive + negative).',
    'Total Tested, Daily Increase': 'Test results (positive + negative) increase from the day before.',
    # total tested per 100k
    'Total Tested per 100k, Cumulative': 'Total cumulative test results (positive + negative), normalized rate to per 100k population.',
    'Total Tested per 100k, Daily Increase': 'Test results (positive + negative) increase from the day before, normalized rate to per 100k population.',
    # deaths
    'Deaths, Cumulative': 'Total cumulative death toll.',
    'Deaths, Daily Increase': 'Death toll increase from the day before.',
    # deaths per 100k
    'Deaths per 100k, Cumulative': 'Total cumulative death toll, normalized rate to per 100k population.',
    'Deaths per 100k, Daily Increase': 'Death toll increase from the day before, normalized rate to per 100k population.',
    # recovered
    'Recovered, Cumulative': 'Total cumulative recoveries.',
    # recovered per 100k
    'Recovered per 100k, Cumulative': 'Total cumulative recoveries, normalized rate to per 100k population.',  
    # hospitalized 
    'Hospitalized, Cumulative': 'Total cumulative hospitalization cases.',
    'Hospitalized, Daily Increase': 'Hospitalization cases increase from the day before.',
    # hospitalized per 100k
    'Hospitalized per 100k, Cumulative': 'Total cumulative hospitalization cases, normalized rate to per 100k population.',
    'Hospitalized per 100k, Daily Increase': 'Hospitalization cases increase from the day before, normalized rate to per 100k population.',
    # in ICU
    'In ICU, Cumulative': 'Total cumulative ICU (Intensive Care Unit) cases.',
    'In ICU, Currently': 'Current ICU (Intensive Care Unit) cases on this day.',
    # in ICU per 100k
    'In ICU per 100k, Cumulative': 'Total cumulative ICU (Intensive Care Unit) cases, normalized rate to per 100k population.',
    'In ICU per 100k, Currently': 'Current ICU (Intensive Care Unit) cases on this day, normalized rate to per 100k population.',
    # on ventilator
    'On Ventilator, Cumulative': 'Total cumulative cases requiring ventilators.',
    'On Ventilator, Currently': 'Current cases requiring ventilators.',
    # on ventilator
    'On Ventilator per 100k, Cumulative': 'Total cumulative cases requiring ventilators, normalized rate to per 100k population.',
    'On Ventilator per 100k, Currently': 'Current cases requiring ventilators, normalized rate to per 100k population.',
}

# US State Populations (2019 Estimate), Source: https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population
STATE_POPULATIONS = {
    'AK': 731545,
    'AL': 4903185,
    'AR': 3017825,
    'AS': 55641,
    'AZ': 7278717,
    'CA': 39512223,
    'CO': 5758736,
    'CT': 3565287,
    'DC': 705749,
    'DE': 973764,
    'FL': 21477737,
    'GA': 10617423,
    'HI': 1415872,
    'IA': 3155070,
    'ID': 1787065,
    'IL': 12671821,
    'IN': 6732219,
    'KS': 2913314,
    'KY': 4467673,
    'LA': 4648794,
    'MA': 6949503,
    'MD': 6045680,
    'ME': 1344212,
    'MI': 9986857,
    'MN': 5639632,
    'MO': 6137428,
    'MP': 55194,
    'MS': 2976149,
    'MT': 1068778,
    'NC': 10488084,
    'ND': 762062,
    'NE': 1934408,
    'NH': 1359711,
    'NJ': 8882190,
    'NM': 2096829,
    'NV': 3080156,
    'NY': 19453561,
    'OH': 11689100,
    'OK': 3956971,
    'OR': 4217737,
    'PA': 12801989,
    'PR': 3193694,
    'RI': 1059361,
    'SC': 5148714,
    'SD': 884659,
    'TN': 6833174,
    'TX': 28995881,
    'UT': 3205958,
    'VA': 8535519,
    'VI': 104914,
    'VT': 623989,
    'WA': 7614893,
    'WI': 5822434,
    'WV': 1792147,
    'WY': 578759
}
US_POPULATION = sum(STATE_POPULATIONS.values())