### CONSTANT VARIABLES

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
    # negative
    {'label': 'Negative, Cumulative', 'value': 'Negative, Cumulative'},
    {'label': 'Negative, Daily Increase', 'value': 'Negative, Daily Increase'},
    # total tested (positive + negative)
    {'label': 'Total Tested, Cumulative', 'value': 'Total Tested, Cumulative'},
    {'label': 'Total Tested, Daily Increase', 'value': 'Total Tested, Daily Increase'},
    # deaths
    {'label': 'Deaths, Cumulative', 'value': 'Deaths, Cumulative'},
    {'label': 'Deaths, Daily Increase', 'value': 'Deaths, Daily Increase'},
    # recovered
    {'label': 'Recovered, Cumulative', 'value': 'Recovered, Cumulative'},
    # hospitalized
    {'label': 'Hospitalized, Cumulative', 'value': 'Hospitalized, Cumulative'},
    {'label': 'Hospitalized, Daily Increase', 'value': 'Hospitalized, Daily Increase'},
    # in ICU
    {'label': 'In ICU, Cumulative', 'value': 'In ICU, Cumulative'},
    {'label': 'In ICU, Currently', 'value': 'In ICU, Currently'},
    # on ventilators
    {'label': 'On Ventilator, Cumulative', 'value': 'On Ventilator, Cumulative'},
    {'label': 'On Ventilator, Currently', 'value': 'On Ventilator, Currently'}
]

# metric definitions, source: https://covidtracking.com/api
METRIC_DEFINITIONS = {
    'Positive, Cumulative': 'Total cumulative positive test results.',
    'Positive, Daily Increase': 'Positive test results increase from the day before.',
    'Negative, Cumulative': 'Total cumulative negative test results.',
    'Negative, Daily Increase': 'Negative test results increase from the day before.',
    'Total Tested, Cumulative': 'Total cumulative test results (positive + negative).',
    'Total Tested, Daily Increase': 'Test results (positive + negative) increase from the day before.',
    'Deaths, Cumulative': 'Total cumulative death toll.',
    'Deaths, Daily Increase': 'Death toll increase from the day before.',
    'Recovered, Cumulative': 'Total cumulative recoveries.',
    'Hospitalized, Cumulative': 'Total cumulative hospitalization cases.',
    'Hospitalized, Daily Increase': 'Hospitalization cases increase from the day before.',
    'In ICU, Cumulative': 'Total cumulative ICU (Intensive Care Unit) cases.',
    'In ICU, Currently': 'Current ICU (Intensive Care Unit) cases on this day.',
    'On Ventilator, Cumulative': 'Total cumulative cases requiring ventilators.',
    'On Ventilator, Currently': 'Current cases requiring ventilators.'
}

# US State Populations (2019 Estimate), Source: https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population
POPULATION_AK = 731545
POPULATION_AL = 4903185
POPULATION_AR = 3017825
POPULATION_AS = 55641
POPULATION_AZ = 7278717
POPULATION_CA = 39512223
POPULATION_C0 = 5758736
POPULATION_CT = 3565287
POPULATION_DC = 705749
POPULATION_DE = 973764
POPULATION_FL = 21477737
POPULATION_GA = 10617423
POPULATION_GU = 165718
POPULATION_HI = 1415872
POPULATION_IA = 3155070
POPULATION_ID = 1787065
POPULATION_IL = 12671821
POPULATION_IN = 6732219
POPULATION_KS = 2913314
POPULATION_KY = 4467673
POPULATION_LA = 4648794
POPULATION_MA = 6949503
POPULATION_MD = 6045680
POPULATION_ME = 1344212
POPULATION_MI = 9986857
POPULATION_MN = 5639632
POPULATION_MO = 6137428
POPULATION_MP = 55194
POPULATION_MS = 2976149
POPULATION_MT = 1068778
POPULATION_NC = 10488084
POPULATION_ND = 762062
POPULATION_NE = 1934408
POPULATION_NH = 1359711
POPULATION_NJ = 8882190
POPULATION_NM = 2096829
POPULATION_NV = 3080156
POPULATION_NY = 19453561
POPULATION_OH = 11689100
POPULATION_OK = 3956971
POPULATION_OR = 4217737
POPULATION_PA = 12801989
POPULATION_PR = 3193694
POPULATION_RI = 1059361
POPULATION_SC = 5148714
POPULATION_SD = 884659
POPULATION_TN = 6833174
POPULATION_TX = 28995881
POPULATION_UT = 3205958
POPULATION_VA = 8535519
POPULATION_VI = 104914
POPULATION_VT = 623989
POPULATION_WA = 7614893
POPULATION_WI = 5822434
POPULATION_WV = 1792147
POPULATION_WY = 578759
POPULATION_US = POPULATION_AK + POPULATION_AL + POPULATION_AR + POPULATION_AS + \
    POPULATION_AZ + POPULATION_CA + POPULATION_C0 + POPULATION_CT + \
    POPULATION_DC + POPULATION_DE + POPULATION_FL + POPULATION_GA + \
    POPULATION_GU + POPULATION_HI + POPULATION_IA + POPULATION_ID + \
    POPULATION_IL + POPULATION_IN + POPULATION_KS + POPULATION_KY + \
    POPULATION_LA + POPULATION_MA + POPULATION_MD + POPULATION_ME + \
    POPULATION_MI + POPULATION_MN + POPULATION_MO + POPULATION_MP + \
    POPULATION_MS + POPULATION_MT + POPULATION_NC + POPULATION_ND + \
    POPULATION_NE + POPULATION_NH + POPULATION_NJ + POPULATION_NM + \
    POPULATION_NV + POPULATION_NY + POPULATION_OH + POPULATION_OK + \
    POPULATION_OR + POPULATION_PA + POPULATION_PR + POPULATION_RI + \
    POPULATION_SC + POPULATION_SD + POPULATION_TN + POPULATION_TX + \
    POPULATION_UT + POPULATION_VA + POPULATION_VI + POPULATION_VT + \
    POPULATION_WA + POPULATION_WI + POPULATION_WV + POPULATION_WY