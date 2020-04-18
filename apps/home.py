import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import DF_STATES, STATES, DF_FEDERAL, DELTA_DAYS, EARLIEST_DATE, LATEST_DATE
from const import METRIC_SELECT_OPTIONS, METRIC_DEFINITIONS
from datetime import datetime, timedelta
from app import app, server
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

gh = {'height': '100px'}

child = [
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
    html.P(
        children = [html.A('Source', href = 'https://covidtracking.com/api'),
        ' updated ', LATEST_DATE.strftime('%Y/%m/%d'),
        ', US only']
    ),
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
                        value = 'Positive, Cumulative'
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
    #html.Div(id = 'metric-table')
    #html.H5(children = 'State Statistics'),
    #dcc.Loading(dcc.Graph(id = 'metric-graph-all-states'), color = '#222222', type = 'circle'),
]

for i in range(17):
    state1, state2, state3 = STATES[3*i], STATES[3*i+1], STATES[3*i+2]
    new_div = html.Div(
        className = 'row',
        children = [
            html.Div(
                className = 'two columns',
                children = [html.H3(html.Strong(id = f'{state1}-metric-info-today')),html.Strong(f'{state1}'), html.P(id = f'{state1}-metric-info-increase')]
            ),
            html.Div(
                className = 'two columns',
                children = dcc.Loading(dcc.Graph(id = f'{state1}-metric-graph', style = gh), color = '#222222', type = 'circle')
            ),
            html.Div(
                className = 'two columns',
                children = [html.H3(html.Strong(id = f'{state2}-metric-info-today')), html.Strong(f'{state2}'), html.P(id = f'{state2}-metric-info-increase')]
            ),
            html.Div(
                className = 'two columns',
                children = dcc.Loading(dcc.Graph(id = f'{state2}-metric-graph', style = gh), color = '#222222', type = 'circle')
            ),
            html.Div(
                className = 'two columns',
                children = [html.H3(html.Strong(id = f'{state3}-metric-info-today')), html.Strong(f'{state3}'), html.P(id = f'{state3}-metric-info-increase')]
            ),
            html.Div(
                className = 'two columns',
                children = dcc.Loading(dcc.Graph(id = f'{state3}-metric-graph', style = gh), color = '#222222', type = 'circle')
            )
        ]
    )
    child.append(new_div)

### APP LAYOUT
layout = html.Div(
    className = 'container',
    children = child
)

# CALLBACK FUNCTIONS
### CALLBACK FUNCTION - METRIC NAME
def update_name(metric):
    return metric
### CALLBACK FUNCTION - METRIC DEFINITION
def update_definition(metric):
    return METRIC_DEFINITIONS[metric]
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

### CALLBACK FUNCTION - GRAPH
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
            color_discrete_sequence = ['#'+(str(hex(i))[-6:]).upper() for i in range(int("0x6A5D96", 0), int("0x965D6C", 0), 51)] if state == 'all' else None,
            height = 600 if state == 'all' else 100
    )
    # edit display
    fig.update_xaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
    fig.update_yaxes(showticklabels=False, visible=False, tickfont=dict(size=1))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    if state == 'all':
        # TODO fix color scheme
        fig.update_layout(legend_orientation='h')
        data_top5 = data.sort_values(by=['Date', metric], ascending=False).head(3).reset_index()
        for i, row in data_top5.iterrows():
            fig.add_annotation(x=row['Date'], y=row[metric], text=f'{row["State"]} - #{i+1}')
        fig.update_annotations(dict(xref="x", yref="y", showarrow=True, arrowhead=7, ax=40, ay=0))
    return fig

def abs_diff(b, a):
    return b - a
def perc_diff(b, a):
    return (b / a - 1) if a != 0 else 0

def update_df(metric, days_since_d1):
    today_info = DF_STATES[DF_STATES['Days Since First Case'] == days_since_d1][['Date', 'State', metric]]
    yesterday_info = DF_STATES[DF_STATES['Days Since First Case'] == (days_since_d1-1)][['Date', 'State', metric]]
    temp = pd.merge(today_info, yesterday_info, how='left', on=['State'], suffixes=(None, '_y'))
    temp['Absolute Difference, Daily'] = temp[[metric, f'{metric}_y']].apply(lambda x:abs_diff(*x), axis=1)
    temp['% Difference, Daily'] = temp[[metric, f'{metric}_y']].apply(lambda x: perc_diff(*x), axis=1)
    temp['% Difference, Daily'] = round(temp['% Difference, Daily']*100, 1)
    temp.drop(columns=['Date_y', f'{metric}_y'], inplace=True)
    temp.sort_values([metric], ascending=False, inplace=True)
    temp.reset_index(drop=True, inplace=True)
    return temp

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
    return update_name(metric), update_definition(metric)

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
    return update_name(metric)

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

'''
##### table
@app.callback(
    Output('metric-table', 'children'),
    [Input('date-slider', 'value'), Input('metric-select', 'value')]
)
def update_netric_table(days_since_d1, metric):
    df = update_df(metric, days_since_d1)
    cols=[{"name": i, "id": i} for i in df.columns]
    da = df.to_dict('records')
    output = dash_table.DataTable(
        columns = cols,
        data = da,
        sort_action='native',
        filter_action='native',
        style_cell={'fontSize':16, 'font-family':'sans-serif'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_as_list_view=True,
    )
    return output

'''
### METRIC PER STATE
##### metric all states - graph
@app.callback(
    Output('metric-graph-all-states', 'figure'),
    [Input('metric-select', 'value'), Input('date-slider', 'value')]
)
def update_metric_graph_all_states(metric, days_since_d1):
    return update_graph('all', metric, days_since_d1)

##### 50 (+DC) invididual states
for state in STATES:
    @app.callback(
        [Output(f'{state}-metric-info-today', 'children'), Output(f'{state}-metric-info-increase', 'children')],
        [Input('metric-select', 'value'), Input('date-slider', 'value')]
    )
    def update_state_info(metric, days_since_d1, state = state):
        return update_info(state, metric, days_since_d1)
    @app.callback(
        Output(f'{state}-metric-graph', 'figure'),
        [Input('metric-select', 'value'), Input('date-slider', 'value')]
    )
    def update_state_graph(metric, days_since_d1, state = state):
        return update_graph(state, metric, days_since_d1)