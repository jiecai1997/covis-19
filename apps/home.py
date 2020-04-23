import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from app import app, server
from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format, Sign
import dash_table.FormatTemplate as FormatTemplate

import pandas as pd
import math

from data.health import DF_STATES, STATES, DF_FEDERAL, DELTA_DAYS, EARLIEST_DATE, LATEST_DATE
from const import METRIC_SELECT_OPTIONS, METRIC_DEFINITIONS
from datetime import datetime, timedelta

gh = {'height': '120px'}

child = [
    # navigation bar
    html.Ul(
        className = 'topnav',
        children = [
            html.Li(html.A(html.B('COVIS19'), className = 'active', href='#')),
            html.Li(html.A('💊Health', className = 'active', href='#')),
            html.Li(html.A('💵Finance', href='/finance')),
            #html.Li(html.A('About', href='/about')),
            html.Li(className = 'right', children=[html.A('💻Github', href='https://github.com/jiecai1997/covis19')])
        ]
    ),
    html.Br(),
    html.P(
        children = ['💊',html.A('Source', href = 'https://covidtracking.com/api'),
        ' updated ', LATEST_DATE.strftime('%Y/%m/%d'),
        ', US COVID-19 cases only.']
    ),
    html.Br(),
    html.H5(children = 'Overall Metrics'),
    html.Div(
        className = 'row',
        children = [
            html.Div(
                className = 'two columns',
                children = [
                    html.H2(html.Strong(id = 'federal-positive-info-today')),
                    html.Strong('Positive, Cumulative'),
                    html.Div(id = 'federal-positive-info-1d'),
                    html.Div(id = 'federal-positive-info-1w')
                ]
            ),
            html.Div(
                className = 'two columns',
                children = dcc.Loading(dcc.Graph(id = 'federal-positive-graph', style = gh), color = '#222222', type = 'circle')
            ),
            html.Div(
                className = 'two columns',
                children = [
                    html.H2(html.Strong(id = 'federal-deaths-info-today')),
                    html.Strong('Deaths, Cumulative'),
                    html.Div(id = 'federal-deaths-info-1d'),
                    html.Div(id = 'federal-deaths-info-1w')
                ]
            ),
            html.Div(
                className = 'two columns',
                children = dcc.Loading(dcc.Graph(id = 'federal-deaths-graph', style = gh), color = '#222222', type = 'circle')
            ),
            html.Div(
                className = 'two columns',
                children = [
                    html.H2(html.Strong(id = 'federal-recovered-info-today')),
                    html.Strong('Recovered, Cumulative'),
                    html.Div(id = 'federal-recovered-info-1d'),
                    html.Div(id = 'federal-recovered-info-1w')
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
                    html.H5('Specific Metric'),
                    html.Strong(id = 'metric-name'),
                    html.P(id = 'metric-definition'), 
                    dcc.Dropdown(
                        id = 'metric-select',
                        options = METRIC_SELECT_OPTIONS,
                        value = 'Positive, Cumulative'
                    ),
                    html.Br(),
                    # metric line graph
                    html.Div(
                        className = 'row',
                        children = [
                            html.Div(
                                className = 'six columns',
                                children = [
                                    html.H2(html.Strong(id = 'federal-metric-info-today')),
                                    html.Strong(id = 'metric-name-2'),
                                    html.Div(id = 'federal-metric-info-1d'),
                                    html.Div(id = 'federal-metric-info-1w'),
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
    dcc.Loading(dcc.Graph(id = 'metric-graph-all-states'), color = '#222222', type = 'circle'),
    html.Br(),
    html.Br(),
    dcc.Loading(dcc.Graph(id = 'metric-graph-individual-states'), color = '#222222', type = 'circle'),
]

child.append(html.Div(id = 'metric-table'))

### APP LAYOUT
layout = html.Div(
    className = 'container',
    children = child
)

# HELPER FUNCTIONS
# absolute difference
def abs_diff(b, a):
    return b - a
# % Delta
def perc_diff(b, a):
    return (b / a - 1) if a != 0 else 0
# info given a certain day
def get_info(state, metric, days_since_d1, days_diff, output):
    if output == 'info':
        if state  == 'federal':
            data = sum(DF_FEDERAL[DF_FEDERAL['Days Since First Case'] == (days_since_d1 - days_diff)][metric])
        else:
            data = sum(DF_STATES[(DF_STATES['State'] == state) & (DF_STATES['Days Since First Case'] == (days_since_d1 - days_diff))][metric])
        data = data if data else 0
    if output == 'graph':
        if state == 'federal':
            data = DF_FEDERAL[DF_FEDERAL['Days Since First Case'] <= (days_since_d1 - days_diff)][['Date', metric]]
        elif state == 'all':
            data = DF_STATES[DF_STATES['Days Since First Case'] <= (days_since_d1 - days_diff)][['Date', 'State', metric]]
            top_3_states = data.sort_values(by=['Date', metric], ascending=False).head(3)['State'].values
            data['Top 3 States'] = data['State'].isin(top_3_states).astype(int)
        elif state == 'all_states':
            data = DF_STATES[DF_STATES['Days Since First Case'] <= (days_since_d1 - days_diff)][['Date', 'State', metric]]
        else:
            data = DF_STATES[(DF_STATES['State'] == state) & (DF_STATES['Days Since First Case'] <= (days_since_d1 - days_diff))][['Date', metric]]
    if output == 'table':
        data = DF_STATES[DF_STATES['Days Since First Case'] == (days_since_d1 - days_diff)][['State', metric]]
    return data
# state annotation function
def annotate(a, metric, days_since_d1):
    state = a.text.split("=")[-1]
    info_today, info_increase_1d, info_increase_1w = update_info(state, metric, days_since_d1)
    return a.update(text = f'<b>{state} {info_today}</b><br>{info_increase_1d}<br>{info_increase_1w}')

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
    info_today = get_info(state, metric, days_since_d1, 0, 'info')
    info_1d = get_info(state, metric, days_since_d1, 1, 'info')
    info_1w = get_info(state, metric, days_since_d1, 7, 'info')

    # calculate difference information
    abs_diff_1d = abs_diff(info_today, info_1d)
    abs_diff_1w = abs_diff(info_today, info_1w)
    perc_diff_1d = perc_diff(info_today, info_1d)
    perc_diff_1w = perc_diff(info_today, info_1w)
    plus_1d = '+' if abs_diff_1d >=0 else ''
    plus_1w = '+' if abs_diff_1w >=0 else ''

    # format for string printing
    info_today = f'{int(info_today):,}'
    info_increase_1d = f'1D | {plus_1d}{int(abs_diff_1d):,}, {plus_1d}{perc_diff_1d:.1%}'
    info_increase_1w = f'1W | {plus_1w}{int(abs_diff_1w):,}, {plus_1w}{perc_diff_1w:.1%}'

    return info_today, info_increase_1d, info_increase_1w

### CALLBACK FUNCTION - GRAPH
def update_graph(state, metric, days_since_d1):
    data = get_info(state, metric, days_since_d1, 0, 'graph')
    if state != 'all_states':
        fig = px.line(
                data, 
                x = 'Date',
                y = metric, 
                line_group = 'State' if state == 'all' else None,
                color = 'Top 3 States' if state == 'all' else None,
                template = 'plotly_white',
                color_discrete_sequence = ['#E2E2E2', '#E45756'] if state == 'all' else ['#E45756'],
                category_orders={'Top 3 States': [0, 1]},
                hover_name= 'State' if state == 'all' else None,
                height = 120 if state != 'all' else 600,
                log_y= True if state == 'all' else False
        )
    elif state == 'all_states':
        fig = px.line(
                data, 
                x = 'Date',
                y = metric,
                hover_name= 'State',
                facet_col = 'State',
                facet_col_wrap = 6,
                color_discrete_sequence = ['#E45756'],
                height = 2600,
                template = 'plotly_white'
        )
        fig.update_yaxes(matches=None)
        fig.for_each_annotation(lambda a: annotate(a, metric, days_since_d1))
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":50})
    # edit display
    if state != 'all':
        fig.update_xaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
        fig.update_yaxes(showticklabels=False, visible=False, tickfont=dict(size=1))
    if state != 'all_states':
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    if state == 'all':
        # add state info
        fig.update_layout(showlegend=False)
        data_top = data.sort_values(by=['Date', metric], ascending=False).head(3).reset_index()
        for i, row in data_top.iterrows():
            fig.add_annotation(x=row['Date'], y=math.log10(row[metric]+0.001), text=f'#{i+1} {row["State"]}')
        # add descriptive info
        max_v = max(data[metric])
        min_v = -1/math.log10(max_v/10)
        fig.update_yaxes(range=[min_v, math.log10(max_v*2)])
        # first death
        if max(data['Date']) >= '2020-02-28':
            fig.add_shape(dict(type="line", x0='2020-02-28', y0=min_v, x1='2020-02-28', y1=max_v, 
                    line=dict(color='Grey', width=0.1, dash="dot")))
            fig.add_annotation(x='2020-02-28', y=math.log10(max_v), text='2/28 - 1st US COVID-19 Death')
        # state of emergency
        if max(data['Date']) >= '2020-03-13':
            fig.add_shape(dict(type="line", x0='2020-03-13', y0=min_v, x1='2020-03-13', y1=max_v, 
                    line=dict(color='Grey', width=0.1, dash="dot")))
            fig.add_annotation(x='2020-03-13', y=math.log10(max_v), text='3/13 - State of Emergency Decleared')
        # US becomes number 1 in cases
        if max(data['Date']) >= '2020-03-26':
            fig.add_shape(dict(type="line", x0='2020-03-26', y0=min_v, x1='2020-03-26', y1=max_v, 
                line=dict(color='Grey', width=0.1, dash="dot")))
            fig.add_annotation(x='2020-03-26', y=math.log10(max_v), text='3/26 - US Leads in COVID-19 Cases')
        # style
        fig.update_annotations(dict(xref="x", yref="y", showarrow=True, arrowhead=7, ax=50, ay=0))
    return fig

### CALLBACK FUNCTION - TABLE
def update_df(metric, days_since_d1):
    info_today = get_info('all', metric, days_since_d1, 0, 'table')
    info_1d = get_info('all', metric, days_since_d1, 1, 'table')
    info_1w = get_info('all', metric, days_since_d1, 7, 'table')
    temp = pd.merge(info_today, info_1d, how='left', on=['State'], suffixes=(None, '_1D'))
    temp = pd.merge(temp, info_1w, how='left', on=['State'], suffixes=(None, '_1W'))
    temp['1D | # Delta'] = temp[[metric, f'{metric}_1D']].apply(lambda x:abs_diff(*x), axis=1)
    temp['1W | # Delta'] = temp[[metric, f'{metric}_1W']].apply(lambda x:abs_diff(*x), axis=1)
    temp['1D | % Delta'] = temp[[metric, f'{metric}_1D']].apply(lambda x: perc_diff(*x), axis=1)
    temp['1W | % Delta'] = temp[[metric, f'{metric}_1W']].apply(lambda x: perc_diff(*x), axis=1)
    temp.drop(columns=[f'{metric}_1D', f'{metric}_1W'], inplace=True)
    temp.sort_values([metric], ascending=False, inplace=True)
    temp.reset_index(drop=True, inplace=True)
    temp['Rank'] = temp.index + 1
    return temp

# CALLBACKS
### KEY 3 METRICS
##### key 3 metrics - numbers
@app.callback(
    [
        Output('federal-positive-info-today', 'children'), 
        Output('federal-positive-info-1d', 'children'),
        Output('federal-positive-info-1w', 'children'),
    ],
    [Input('date-slider', 'value')]
)
def update_federal_positive_info(days_since_d1):
    return update_info('federal', 'Positive, Cumulative', days_since_d1)

@app.callback(
    [
        Output('federal-deaths-info-today', 'children'), 
        Output('federal-deaths-info-1d', 'children'),
        Output('federal-deaths-info-1w', 'children'),
    ],
    [Input('date-slider', 'value')]
)
def update_federal_deaths_info(days_since_d1):
    return update_info('federal', 'Deaths, Cumulative', days_since_d1)

@app.callback(
    [
        Output('federal-recovered-info-today', 'children'), 
        Output('federal-recovered-info-1d', 'children'),
        Output('federal-recovered-info-1w', 'children'),
    ],
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
    days_since_d1_output = f'{days_since_d1} day(s) since first US COVID-19 death.'
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
        Output('federal-metric-info-today', 'children'), 
        Output('federal-metric-info-1d', 'children'),
        Output('federal-metric-info-1w', 'children'),
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
        color_continuous_scale = 'OrRd',
        labels = {metric: ''}
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

##### metric graph all states
@app.callback(
    Output('metric-graph-all-states', 'figure'),
    [Input('date-slider', 'value'), Input('metric-select', 'value')]
)
def update_all_states_graph(days_since_d1, metric):
    return update_graph('all', metric, days_since_d1)

@app.callback(
    Output('metric-graph-individual-states', 'figure'),
    [Input('date-slider', 'value'), Input('metric-select', 'value')]
)
def update_individual_states_graph(days_since_d1, metric):
    return update_graph('all_states', metric, days_since_d1)

##### states table
@app.callback(
    Output('metric-table', 'children'),
    [Input('date-slider', 'value'), Input('metric-select', 'value')]
)
def update_netric_table(days_since_d1, metric):
    df = update_df(metric, days_since_d1)
    cols=[
        {'name': 'Rank', 'id': 'Rank', 'type': 'numeric'},
        {'name': 'State', 'id': 'State'},
        {'name': metric, 'id': metric, 'type': 'numeric', 'format': Format(group=',')},
        {'name': '1D | # Delta', 'id': '1D | # Delta', 'type': 'numeric', 'format': Format(group=',')},
        {'name': '1W | # Delta', 'id': '1W | # Delta', 'type': 'numeric', 'format': Format(group=',')},
        {'name': '1D | % Delta', 'id': '1D | % Delta', 'type': 'numeric', 'format': FormatTemplate.percentage(1).sign(Sign.positive)},
        {'name': '1W | % Delta', 'id': '1W | % Delta', 'type': 'numeric', 'format': FormatTemplate.percentage(1).sign(Sign.positive)}
    ]
    da = df.to_dict('records')
    output = dash_table.DataTable(
        columns = cols,
        data = da,
        sort_action='native',
        filter_action='native',
        style_cell={'fontSize':15, 'font-family':'sans-serif', 'textAlign': 'left', 'padding':'10px'},
        style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},
        style_as_list_view=True,
    )
    return output