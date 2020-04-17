import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import DF_STATES, DF_FEDERAL, DELTA_DAYS, EARLIEST_DATE, LATEST_DATE
from const import METRIC_SELECT_OPTIONS, METRIC_DEFINITIONS
from datetime import datetime, timedelta
from app import app
from dash.dependencies import Input, Output
import time

gh = {'height': '100px'}

### APP LAYOUT
layout = html.Div(
    className = 'container',
    children=[

        # navigation bar
        html.Ul(
            className = 'topnav',
            children = [
                html.Li(html.A(html.B('COVIS19'), className = 'active', href='#')),
                html.Li(html.A('About', href='/about')),
                html.Li(className = 'right', children=[html.A('Github', href='https://github.com/jiecai1997/covis19')])
            ]
        ),

        html.Br(),
        
        html.H5(children = '💊Overall Statistics'),
        html.P(children = [
            html.A('Source', href = 'https://covidtracking.com/api'),
            ' updated ', LATEST_DATE.strftime('%Y/%m/%d'),
            ', US only']),
    
        html.Br(),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [
                        html.H1(html.Strong(id = 'federal-positive-info-today')),
                        html.Strong('Positive, Cumulative'),
                        html.P(id = 'federal-positive-info-increase')
                    ]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'federal-positive-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [
                        html.H1(html.Strong(id = 'federal-deaths-info-today')),
                        html.Strong('Deaths, Cumulative'),
                        html.P(id = 'federal-deaths-info-increase')
                    ]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'federal-deaths-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [
                        html.H1(html.Strong(id = 'federal-recovered-info-today')),
                        html.Strong('Recovered, Cumulative'),
                        html.P(id = 'federal-recovered-info-increase')
                    ]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'federal-recovered-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Hr(),

        # metrics top section
        html.Div(
            className = 'row',
            children = [   
                html.Div(
                    className = 'four columns',
                    children = [
                        # date
                        html.H5('Date'),
                        html.Strong(id = 'date-output'),
                        html.P(id = 'days-since-d1-output'),
                        dcc.Slider(
                            id = 'date-slider',
                            min = 0,
                            max = DELTA_DAYS,
                            marks = {i:(EARLIEST_DATE + timedelta(days=i)).strftime('%Y/%m/%d') \
                                for i in range(int(DELTA_DAYS/4), (DELTA_DAYS+1-int(DELTA_DAYS/4)), int(DELTA_DAYS/2))},
                            value = DELTA_DAYS
                        ),
                        html.Br(),
                        html.Br(),
                        # metric
                        html.H5('Metric'),
                        html.Strong(id = 'metric-name'),
                        html.P(id = 'metric-definition'), 
                        dcc.Dropdown(
                            id = 'metric-select',
                            options = METRIC_SELECT_OPTIONS,
                            value = 'Positive, Daily Increase'
                        ),
                        html.Br(),
                        html.Br(),
                        # metric line graph
                        html.Div(
                            className = 'row',
                            children = [
                                html.Div(
                                    className = 'six columns',
                                    children = [
                                        html.H1(html.Strong(id = 'federal-metrics-info-today')),
                                        html.Strong(id = 'metric-name-2'),
                                        html.P(id = 'federal-metrics-info-increase')
                                    ]
                                ),
                                html.Div(
                                    className = 'six columns',
                                    children = [
                                        dcc.Loading(dcc.Graph(id = 'federal-metrics-graph', style = gh), color = '#222222', type = 'circle')
                                    ]
                                )
                            ]
                        )  
                    ]
                ),
                html.Div(
                    className = 'eight columns',
                    children = dcc.Loading(dcc.Graph(id = 'metric-map'), color = '#222222', type = 'circle')
                )
            ]
        ),
        html.Hr(),
        html.H5(children = 'State Statistics'),
        #dcc.Loading(dcc.Graph(id = 'metric-graph-all-states'), color = '#222222', type = 'circle'),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'AK-metric-info-today')),html.Strong('AK, Alaska'), html.P(id = 'AK-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'AK-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'AL-metric-info-today')), html.Strong('AL, Alabama'), html.P(id = 'AL-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'AL-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'AR-metric-info-today')), html.Strong('AR, Arkansas'), html.P(id = 'AR-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'AR-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),    

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'AZ-metric-info-today')), html.Strong('AZ, Arizona'), html.P(id = 'AZ-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'AZ-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'CA-metric-info-today')), html.Strong('CA, California'), html.P(id = 'CA-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'CA-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'CO-metric-info-today')), html.Strong('CO, Colorado'), html.P(id = 'CO-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'CO-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'CT-metric-info-today')), html.Strong('CT, Connecticut'), html.P(id = 'CT-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'CT-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'DC-metric-info-today')), html.Strong('DC, Washington DC'), html.P(id = 'DC-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'DC-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'DE-metric-info-today')), html.Strong('DE, Delaware'), html.P(id = 'DE-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'DE-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'FL-metric-info-today')), html.Strong('FL, Florida'), html.P(id = 'FL-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'FL-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'GA-metric-info-today')), html.Strong('GA, Georgia'), html.P(id = 'GA-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'GA-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'HI-metric-info-today')), html.Strong('HI, Hawaii'), html.P(id = 'HI-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'HI-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'IA-metric-info-today')), html.Strong('IA, Iowa'), html.P(id = 'IA-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'IA-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'ID-metric-info-today')), html.Strong('ID, Idaho'), html.P(id = 'ID-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'ID-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'IL-metric-info-today')), html.Strong('IL, Illonois'), html.P(id = 'IL-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'IL-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'IN-metric-info-today')), html.Strong('IN, Indiana'), html.P(id = 'IN-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'IN-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'KS-metric-info-today')), html.Strong('KS, Kansas'), html.P(id = 'KS-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'KS-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'KY-metric-info-today')), html.Strong('KY, Kentucky'), html.P(id = 'KY-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'KY-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'LA-metric-info-today')), html.Strong('LA, Lousiana'), html.P(id = 'LA-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'LA-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'MA-metric-info-today')), html.Strong('MA, Massachusetts'), html.P(id = 'MA-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'MA-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'MD-metric-info-today')), html.Strong('MD, Maryland'), html.P(id = 'MD-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'MD-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'ME-metric-info-today')), html.Strong('ME, Maine'), html.P(id = 'ME-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'ME-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'MI-metric-info-today')), html.Strong('MI, Michigan'), html.P(id = 'MI-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'MI-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'MN-metric-info-today')), html.Strong('MN, Minnesota'), html.P(id = 'MN-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'MN-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'MO-metric-info-today')), html.Strong('MO, Missouri'), html.P(id = 'MO-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'MO-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'MS-metric-info-today')), html.Strong('MS, Mississippi'), html.P(id = 'MS-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'MS-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'MT-metric-info-today')), html.Strong('MT, Montana'), html.P(id = 'MT-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'MT-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'NC-metric-info-today')), html.Strong('NC, North Carolina'), html.P(id = 'NC-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'NC-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'ND-metric-info-today')), html.Strong('ND, North Dakota'), html.P(id = 'ND-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'ND-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'NE-metric-info-today')), html.Strong('NE, Nebraska'), html.P(id = 'NE-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'NE-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'NH-metric-info-today')), html.Strong('NH, New Hampshire'), html.P(id = 'NH-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'NH-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'NJ-metric-info-today')), html.Strong('NJ, New Jersey'), html.P(id = 'NJ-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'NJ-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'NM-metric-info-today')), html.Strong('NM, New Mexico'), html.P(id = 'NM-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'NM-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),

        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'NV-metric-info-today')), html.Strong('NV, Nevada'), html.P(id = 'NV-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'NV-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'NY-metric-info-today')), html.Strong('NY, New York'), html.P(id = 'NY-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'NY-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [html.H3(html.Strong(id = 'OH-metric-info-today')), html.Strong('OH, Ohio'), html.P(id = 'OH-metric-info-increase')]
                ),
                html.Div(
                    className = 'two columns',
                    children = dcc.Loading(dcc.Graph(id = 'OH-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        )
    ]
)

'''
x through 0-16, (3*x)
'''

# CALLBACK FUNCTIONS
### CALLBACK FUNCTION - NUMBERS
def update_info(state, metric, days_since_d1):
    # calculate basic information
    if state == 'federal':
        today_info = sum(DF_FEDERAL[DF_FEDERAL['Days Since First Case'] == days_since_d1][metric])
        yesterday_info = sum(DF_FEDERAL[DF_FEDERAL['Days Since First Case'] == (days_since_d1 - 1)][metric])
    else:
        today_info = sum(DF_STATES[(DF_STATES['State'] == state) & (DF_STATES['Days Since First Case'] == days_since_d1)][metric])
        yesterday_info = sum(DF_STATES[(DF_STATES['State'] == state) & (DF_STATES['Days Since First Case'] == (days_since_d1 - 1))][metric])
    yesterday_info = yesterday_info if yesterday_info else 0

    # calculate difference information
    abs_diff = today_info - yesterday_info
    perc_diff = (today_info / yesterday_info - 1) if yesterday_info != 0 else 0
    plus = '+' if abs_diff >=0 else ''

    # format for string printing
    today_info = f'{int(today_info):,}'
    increase_info = f'{plus}{int(abs_diff):,}, {perc_diff:.1%}'

    return today_info, increase_info

### CALLBACK FUNCTION - NUMBERS
def update_graph(state, metric, days_since_d1):
    # make figure
    if state == 'federal':
        data = DF_FEDERAL[DF_FEDERAL['Days Since First Case'] <= days_since_d1][['Date', metric]]
    elif state == 'all':
        data = DF_STATES[DF_STATES['Days Since First Case'] <= days_since_d1][['Date', 'State', metric]]
    else:
        data = DF_STATES[(DF_STATES['State'] == state) & (DF_STATES['Days Since First Case'] <= days_since_d1)][['Date', metric]]
    fig = px.line(
            data, 
            x = 'Date',
            y = metric, 
            color = 'State' if state == 'all' else None,
            template = 'plotly_white',
            color_discrete_map = {metric: 'Orange'},
            height = 500 if state == 'all' else 100
    )
    # edit display
    fig.update_xaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
    fig.update_yaxes(showticklabels=False, visible=False, tickfont=dict(size=1))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    if state == 'all':
        # TODO fix color scheme
        fig.update_layout(legend_orientation='h')

    return fig

# CALLBACKS
### KEY 3 METRICS
##### key 3 metrics - numbers
@app.callback(
    [Output('federal-positive-info-today', 'children'), Output('federal-positive-info-increase', 'children')],
    [Input('date-slider', 'value')]
)
def update_federal_positive_info(days_since_d1):
    return update_info('federal', 'Positive, Cumulative', days_since_d1)

@app.callback(
    [Output('federal-deaths-info-today', 'children'), Output('federal-deaths-info-increase', 'children')],
    [Input('date-slider', 'value')]
)
def update_federal_deaths_info(days_since_d1):
    return update_info('federal', 'Deaths, Cumulative', days_since_d1)

@app.callback(
    [Output('federal-recovered-info-today', 'children'), Output('federal-recovered-info-increase', 'children')],
    [Input('date-slider', 'value')]
)
def update_federal_recovered_info(days_since_d1):
    return update_info('federal', 'Recovered, Cumulative', days_since_d1)

##### key 3 metrics - graphs
@app.callback(
    Output('federal-positive-graph', 'figure'),
    [Input('date-slider', 'value')]
)
def update_federal_positive_graph(days_since_d1):
    return update_graph('federal', 'Positive, Cumulative', days_since_d1)

@app.callback(
    Output('federal-deaths-graph', 'figure'),
    [Input('date-slider', 'value')]
)
def update_federal_deaths_graph(days_since_d1):
    return update_graph('federal', 'Deaths, Cumulative', days_since_d1)

@app.callback(
    Output('federal-recovered-graph', 'figure'),
    [Input('date-slider', 'value')]
)
def update_federal_recovered_graph(days_since_d1):
    return update_graph('federal', 'Recovered, Cumulative', days_since_d1)

### DATE & METRIC SELECTION
##### date selection
@app.callback(
    [Output('date-output', 'children'), Output('days-since-d1-output', 'children')],
    [Input('date-slider', 'value')]
)
def update_dates_display(days_since_d1):
    date_output = f'{(EARLIEST_DATE + timedelta(days=days_since_d1)).strftime("%Y/%m/%d")}'
    days_since_d1_output = f'{days_since_d1} day(s) since first US COVID-19 case.'
    return date_output, days_since_d1_output

##### metric selection
@app.callback(
    [
        Output('metric-name', 'children'),
        Output('metric-definition', 'children')
    ],
    [Input('metric-select', 'value')]
)
def update_metric_display(metric):
    metric_info = METRIC_DEFINITIONS[metric]
    return metric, metric_info

### METRIC OVERALL
##### metric overall - info
@app.callback(
    [
        Output('federal-metrics-info-today', 'children'), 
        Output('federal-metrics-info-increase', 'children'),
    ],
    [Input('date-slider', 'value'), Input('metric-select', 'value')]
)
def update_federal_metrics_info(days_since_d1, metric):
    return update_info('federal', metric, days_since_d1)
@app.callback(
    Output('metric-name-2', 'children'),
    [Input('metric-select', 'value')]
)
def update_metric_display_2(metric):
    return metric

##### metric overall - federal graph
@app.callback(
    Output('federal-metrics-graph', 'figure'),
    [Input('date-slider', 'value'), Input('metric-select', 'value')]
)
def update_federal_metrics_graph(days_since_d1, metric):
    return update_graph('federal', metric, days_since_d1)

##### metric overall - map
@app.callback(
    Output('metric-map', 'figure'),
    [Input('date-slider', 'value'), Input('metric-select', 'value')]
)
def update_metric_map(days_since_d1, metric):
    data = DF_STATES[DF_STATES['date'] == EARLIEST_DATE + timedelta(days=days_since_d1)][['State', metric]]
    fig = px.choropleth(
        data,
        color = metric,
        locations = 'State',
        range_color = (0, max(DF_STATES[metric])),
        locationmode = 'USA-states',
        scope = 'usa',
        color_continuous_scale = 'Oranges',
        labels = {metric: ''}
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

### METRIC PER STATE
##### metric all states - graph
@app.callback(
    Output('metric-graph-all-states', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_metric_graph_all_states(metric, days_since_d1):
    return update_graph('all', metric, days_since_d1)

##### states specific info
####### AK
@app.callback(
    [Output('AK-metric-info-today', 'children'), Output('AK-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_AK_info(metric, days_since_d1):
    return update_info('AK', metric, days_since_d1)
@app.callback(
    Output('AK-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_AK_graph(metric, days_since_d1):
    return update_graph('AK', metric, days_since_d1)

####### AL
@app.callback(
    [Output('AL-metric-info-today', 'children'), Output('AL-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_AL_info(metric, days_since_d1):
    return update_info('AL', metric, days_since_d1)
@app.callback(
    Output('AL-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_AL_graph(metric, days_since_d1):
    return update_graph('AL', metric, days_since_d1)

####### AR
@app.callback(
    [Output('AR-metric-info-today', 'children'), Output('AR-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_AR_info(metric, days_since_d1):
    return update_info('AR', metric, days_since_d1)
@app.callback(
    Output('AR-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_AR_graph(metric, days_since_d1):
    return update_graph('AR', metric, days_since_d1)

####### AZ
@app.callback(
    [Output('AZ-metric-info-today', 'children'), Output('AZ-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_AZ_info(metric, days_since_d1):
    return update_info('AZ', metric, days_since_d1)
@app.callback(
    Output('AZ-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_AZ_graph(metric, days_since_d1):
    return update_graph('AZ', metric, days_since_d1)

#######CA
@app.callback(
    [Output('CA-metric-info-today', 'children'), Output('CA-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_CA_info(metric, days_since_d1):
    return update_info('CA', metric, days_since_d1)
@app.callback(
    Output('CA-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_CA_graph(metric, days_since_d1):
    return update_graph('CA', metric, days_since_d1)

######## CO
@app.callback(
    [Output('CO-metric-info-today', 'children'), Output('CO-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_CO_info(metric, days_since_d1):
    return update_info('CO', metric, days_since_d1)
@app.callback(
    Output('CO-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_CO_graph(metric, days_since_d1):
    return update_graph('CO', metric, days_since_d1)

######## CT
@app.callback(
    [Output('CT-metric-info-today', 'children'), Output('CT-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_CT_info(metric, days_since_d1):
    return update_info('CT', metric, days_since_d1)
@app.callback(
    Output('CT-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_CT_graph(metric, days_since_d1):
    return update_graph('CT', metric, days_since_d1)

######## DC
@app.callback(
    [Output('DC-metric-info-today', 'children'), Output('DC-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_DC_info(metric, days_since_d1):
    return update_info('DC', metric, days_since_d1)
@app.callback(
    Output('DC-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_DC_graph(metric, days_since_d1):
    return update_graph('DC', metric, days_since_d1)

######## DE
@app.callback(
    [Output('DE-metric-info-today', 'children'), Output('DE-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_DE_info(metric, days_since_d1):
    return update_info('DE', metric, days_since_d1)
@app.callback(
    Output('DE-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_DE_graph(metric, days_since_d1):
    return update_graph('DE', metric, days_since_d1)

######## FL
@app.callback(
    [Output('FL-metric-info-today', 'children'), Output('FL-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_FL_info(metric, days_since_d1):
    return update_info('FL', metric, days_since_d1)
@app.callback(
    Output('FL-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_FL_graph(metric, days_since_d1):
    return update_graph('FL', metric, days_since_d1)

######## GA
@app.callback(
    [Output('GA-metric-info-today', 'children'), Output('GA-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_GA_info(metric, days_since_d1):
    return update_info('GA', metric, days_since_d1)
@app.callback(
    Output('GA-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_GA_graph(metric, days_since_d1):
    return update_graph('GA', metric, days_since_d1)

######## HI
@app.callback(
    [Output('HI-metric-info-today', 'children'), Output('HI-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_HI_info(metric, days_since_d1):
    return update_info('HI', metric, days_since_d1)
@app.callback(
    Output('HI-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_HI_graph(metric, days_since_d1):
    return update_graph('HI', metric, days_since_d1)

######## IA
@app.callback(
    [Output('IA-metric-info-today', 'children'), Output('IA-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_IA_info(metric, days_since_d1):
    return update_info('IA', metric, days_since_d1)
@app.callback(
    Output('IA-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_IA_graph(metric, days_since_d1):
    return update_graph('IA', metric, days_since_d1)

######## ID
@app.callback(
    [Output('ID-metric-info-today', 'children'), Output('ID-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_ID_info(metric, days_since_d1):
    return update_info('ID', metric, days_since_d1)
@app.callback(
    Output('ID-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_ID_graph(metric, days_since_d1):
    return update_graph('ID', metric, days_since_d1)

######## IL
@app.callback(
    [Output('IL-metric-info-today', 'children'), Output('IL-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_IL_info(metric, days_since_d1):
    return update_info('IL', metric, days_since_d1)
@app.callback(
    Output('IL-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_IL_graph(metric, days_since_d1):
    return update_graph('IL', metric, days_since_d1)

######## IN
@app.callback(
    [Output('IN-metric-info-today', 'children'), Output('IN-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_IN_info(metric, days_since_d1):
    return update_info('IN', metric, days_since_d1)
@app.callback(
    Output('IN-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_IN_graph(metric, days_since_d1):
    return update_graph('IN', metric, days_since_d1)

######## KS
@app.callback(
    [Output('KS-metric-info-today', 'children'), Output('KS-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_KS_info(metric, days_since_d1):
    return update_info('KS', metric, days_since_d1)
@app.callback(
    Output('KS-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_KS_graph(metric, days_since_d1):
    return update_graph('KS', metric, days_since_d1)

######## KY
@app.callback(
    [Output('KY-metric-info-today', 'children'), Output('KY-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_KY_info(metric, days_since_d1):
    return update_info('KY', metric, days_since_d1)
@app.callback(
    Output('KY-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_KY_graph(metric, days_since_d1):
    return update_graph('KY', metric, days_since_d1)

######## LA
@app.callback(
    [Output('LA-metric-info-today', 'children'), Output('LA-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_LA_info(metric, days_since_d1):
    return update_info('LA', metric, days_since_d1)
@app.callback(
    Output('LA-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_LA_graph(metric, days_since_d1):
    return update_graph('LA', metric, days_since_d1)

######## MA
@app.callback(
    [Output('MA-metric-info-today', 'children'), Output('MA-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MA_info(metric, days_since_d1):
    return update_info('MA', metric, days_since_d1)
@app.callback(
    Output('MA-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MA_graph(metric, days_since_d1):
    return update_graph('MA', metric, days_since_d1)

######## MD
@app.callback(
    [Output('MD-metric-info-today', 'children'), Output('MD-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MD_info(metric, days_since_d1):
    return update_info('MD', metric, days_since_d1)
@app.callback(
    Output('MD-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MD_graph(metric, days_since_d1):
    return update_graph('MD', metric, days_since_d1)

######## ME
@app.callback(
    [Output('ME-metric-info-today', 'children'), Output('ME-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_ME_info(metric, days_since_d1):
    return update_info('ME', metric, days_since_d1)
@app.callback(
    Output('ME-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_ME_graph(metric, days_since_d1):
    return update_graph('ME', metric, days_since_d1)

######## MI
@app.callback(
    [Output('MI-metric-info-today', 'children'), Output('MI-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MI_info(metric, days_since_d1):
    return update_info('MI', metric, days_since_d1)
@app.callback(
    Output('MI-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MI_graph(metric, days_since_d1):
    return update_graph('MI', metric, days_since_d1)

######## MN
@app.callback(
    [Output('MN-metric-info-today', 'children'), Output('MN-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MN_info(metric, days_since_d1):
    return update_info('MN', metric, days_since_d1)
@app.callback(
    Output('MN-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MN_graph(metric, days_since_d1):
    return update_graph('MN', metric, days_since_d1)

######## MO
@app.callback(
    [Output('MO-metric-info-today', 'children'), Output('MO-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MO_info(metric, days_since_d1):
    return update_info('MO', metric, days_since_d1)
@app.callback(
    Output('MO-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MO_graph(metric, days_since_d1):
    return update_graph('MO', metric, days_since_d1)

######## MS
@app.callback(
    [Output('MS-metric-info-today', 'children'), Output('MS-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MS_info(metric, days_since_d1):
    return update_info('MS', metric, days_since_d1)
@app.callback(
    Output('MS-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MS_graph(metric, days_since_d1):
    return update_graph('MS', metric, days_since_d1)

######## MT
@app.callback(
    [Output('MT-metric-info-today', 'children'), Output('MT-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MT_info(metric, days_since_d1):
    return update_info('MT', metric, days_since_d1)
@app.callback(
    Output('MT-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_MT_graph(metric, days_since_d1):
    return update_graph('MT', metric, days_since_d1)

######## NC
@app.callback(
    [Output('NC-metric-info-today', 'children'), Output('NC-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NC_info(metric, days_since_d1):
    return update_info('NC', metric, days_since_d1)
@app.callback(
    Output('NC-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NC_graph(metric, days_since_d1):
    return update_graph('NC', metric, days_since_d1)

######## ND
@app.callback(
    [Output('ND-metric-info-today', 'children'), Output('ND-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_ND_info(metric, days_since_d1):
    return update_info('ND', metric, days_since_d1)
@app.callback(
    Output('ND-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_ND_graph(metric, days_since_d1):
    return update_graph('ND', metric, days_since_d1)

######## NE
@app.callback(
    [Output('NE-metric-info-today', 'children'), Output('NE-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NE_info(metric, days_since_d1):
    return update_info('NE', metric, days_since_d1)
@app.callback(
    Output('NE-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NE_graph(metric, days_since_d1):
    return update_graph('NE', metric, days_since_d1)

######## NH
@app.callback(
    [Output('NH-metric-info-today', 'children'), Output('NH-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NH_info(metric, days_since_d1):
    return update_info('NH', metric, days_since_d1)
@app.callback(
    Output('NH-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NH_graph(metric, days_since_d1):
    return update_graph('NH', metric, days_since_d1)

######## NJ
@app.callback(
    [Output('NJ-metric-info-today', 'children'), Output('NJ-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NJ_info(metric, days_since_d1):
    return update_info('NJ', metric, days_since_d1)
@app.callback(
    Output('NJ-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NJ_graph(metric, days_since_d1):
    return update_graph('NJ', metric, days_since_d1)

######## NM
@app.callback(
    [Output('NM-metric-info-today', 'children'), Output('NM-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NM_info(metric, days_since_d1):
    return update_info('NM', metric, days_since_d1)
@app.callback(
    Output('NM-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NM_graph(metric, days_since_d1):
    return update_graph('NM', metric, days_since_d1)

######## NV
@app.callback(
    [Output('NV-metric-info-today', 'children'), Output('NV-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NV_info(metric, days_since_d1):
    return update_info('NV', metric, days_since_d1)
@app.callback(
    Output('NV-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NV_graph(metric, days_since_d1):
    return update_graph('NV', metric, days_since_d1)

######## NY
@app.callback(
    [Output('NY-metric-info-today', 'children'), Output('NY-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NY_info(metric, days_since_d1):
    return update_info('NY', metric, days_since_d1)
@app.callback(
    Output('NY-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_NY_graph(metric, days_since_d1):
    return update_graph('NY', metric, days_since_d1)

######## OH
@app.callback(
    [Output('OH-metric-info-today', 'children'), Output('OH-metric-info-increase', 'children')],
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_OH_info(metric, days_since_d1):
    return update_info('OH', metric, days_since_d1)
@app.callback(
    Output('OH-metric-graph', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_OH_graph(metric, days_since_d1):
    return update_graph('OH', metric, days_since_d1)