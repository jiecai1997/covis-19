import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import DF_STATES, DF_FEDERAL, DELTA_DAYS, EARLIEST_DATE, LATEST_DATE
from const import METRIC_SELECT_OPTIONS, METRIC_DEFINITIONS
from datetime import datetime, timedelta
from app import app
from dash.dependencies import Input, Output
import time

colors = {
    'background': '#FFFFFF',
    'text': '#444444'
}

my_style = {
    'textAlign': 'center',
    'color': colors['text']
}

### FUNCTIONS
'''
def generate_table(dataframe, max_rows=56):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ]
)
'''

### APP LAYOUT
layout = html.Div(
    className = 'container',
    #style={'backgroundColor': colors['background']},
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

        #html.H1(html.B('COVIS19 = COVID19 + DATAVIS')),
        #html.P(f"Last Updated {LATEST_DATE.strftime('%Y/%m/%d')}"),

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
                        html.H1(html.Strong(id = 'stats-today-info-positive')),
                        html.Strong('Positive, Cumulative'),
                        html.P(id = 'stats-increase-info-positive')
                    ]
                ),
                html.Div(
                    className = 'two columns',
                    children = [dcc.Graph(id = 'graph-positive')]
                ),
                html.Div(
                    className = 'two columns',
                    children = [
                        html.H1(html.Strong(id = 'stats-today-info-deaths')),
                        html.Strong('Deaths, Cumulative'),
                        html.P(id = 'stats-increase-info-deaths')
                    ]
                ),
                html.Div(
                    className = 'two columns',
                    children = [dcc.Graph(id = 'graph-deaths')]
                ),
                html.Div(
                    className = 'two columns',
                    children = [
                        html.H1(html.Strong(id = 'stats-today-info-recovered')),
                        html.Strong('Recovered, Cumulative'),
                        html.P(id = 'stats-increase-info-recovered')
                    ]
                ),
                html.Div(
                    className = 'two columns',
                    children = [dcc.Graph(id = 'graph-recovered')]
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
                                for i in range(int(DELTA_DAYS/4), DELTA_DAYS-int(DELTA_DAYS/4), int(DELTA_DAYS/2))},
                            value = DELTA_DAYS
                        ),
                        html.Br(),
                        # metric
                        html.H5('Metric'),
                        html.Strong(id = 'metric-name-output'),
                        html.P(id = 'metric-info-output'), 
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
                                        html.H1(html.Strong(id = 'metric-today-info')),
                                        html.Strong(id = 'metric-info'),
                                        html.P(id = 'metric-increase-info')
                                    ]
                                ),
                                html.Div(
                                    className = 'six columns',
                                    children = [
                                        dcc.Graph(id = 'graph-metric')
                                    ]
                                )
                            ]
                        )  
                    ]
                ),
                html.Div(
                    className = 'eight columns',
                    children = [dcc.Graph(id = 'map-interactive')]
                )
            ]
        ),
        html.Hr(),
        '''
        # interactive map
        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'six columns',
                    children = [
                        html.H5(children = 'Interactive Map'),
                        dcc.Graph(id = 'map-interactive')
                    ]
                ),
                html.Div(
                    className = 'six columns',
                    children = [
                        html.H5(children = 'Time Lapse Map'),
                        dcc.Graph(id = 'map-time-lapse')
                    ]
                )                
            ]
        )
        '''
        #generate_table(DF)
    ]
)

### APP CALLBACKS
# update map
@app.callback(
    Output('map-interactive', 'figure'),
    [
        Input('date-slider', 'value'),
        Input('metric-select', 'value')
    ]
)
def update_maps(days_since_d1, metric):

    # map without animation
    map_interactive = px.choropleth(
        DF_STATES[DF_STATES['date'] == EARLIEST_DATE + timedelta(days=days_since_d1)],

        # dynamic
        color = metric,
        locations = 'State',
        range_color = (0, max(DF_STATES[metric])),

        # static
        locationmode = 'USA-states',
        scope = 'usa',
        color_continuous_scale = 'Oranges'
    )
    '''
     # map with animation
    map_time_lapse = px.choropleth(
        #DF[DF['date'] == EARLIEST_DATE + timedelta(days=i)],
        DF.sort_values(by=['date']),

        # dynamic
        color = metric,
        locations = 'State',
        range_color = (0, max(DF[metric])),

        # static
        locationmode = 'USA-states',
        scope = 'usa',
        height = 525,
        animation_frame = 'Date',
        animation_group = metric,
        color_continuous_scale = 'Oranges'
    )
    '''

    #map_time_lapse.update_layout(showlegend=False)
    map_interactive.update_layout(legend_title=''),
    map_interactive.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return map_interactive

# update date display
@app.callback(
    [
        Output('date-output', 'children'),
        Output('days-since-d1-output', 'children')
    ],
    [Input('date-slider', 'value')]
)
def update_dates_display(days_since_d1):
    date_output = f'{(EARLIEST_DATE + timedelta(days=days_since_d1)).strftime("%Y/%m/%d")}'
    days_since_d1_output = f'{days_since_d1} day(s) since first US COVID-19 case.'
    return date_output, days_since_d1_output

# update metric display
@app.callback(
    [
        Output('metric-name-output', 'children'),
        Output('metric-info-output', 'children')
    ],
    [Input('metric-select', 'value')]
)
def update_metric_display(metric):
    metric_info = METRIC_DEFINITIONS[metric]
    return metric, metric_info

# update overall stats display
@app.callback(
    [
        Output('stats-today-info-positive', 'children'),
        Output('stats-increase-info-positive', 'children'),
        Output('stats-today-info-deaths', 'children'),
        Output('stats-increase-info-deaths', 'children'),
        Output('stats-today-info-recovered', 'children'),
        Output('stats-increase-info-recovered', 'children'),
    ],
    [Input('date-slider', 'value')]
)
# TODO replace DF_STATES with DF_FEDERAL cause all these are on national level
def update_overall_stats_display(days_since_d1):
    # calculate metrics
    # current day's info

    df_federal_today = DF_FEDERAL[DF_FEDERAL['Days Since First Case'] == days_since_d1]
    today_info_positive = sum(df_federal_today['Positive, Cumulative'])
    today_info_deaths = sum(df_federal_today['Deaths, Cumulative'])
    today_info_recovered = sum(df_federal_today['Recovered, Cumulative'])
    

    # previous day's info
    df_federal_yesterday = DF_FEDERAL[DF_FEDERAL['Days Since First Case'] == (days_since_d1 -1)]
    yesterday_info_positive = sum(df_federal_yesterday['Positive, Cumulative'])
    yesterday_info_deaths = sum(df_federal_yesterday['Deaths, Cumulative'])
    yesterday_info_recovered = sum(df_federal_yesterday['Recovered, Cumulative'])
    
    yesterday_info_positive = yesterday_info_positive if yesterday_info_positive else 0
    yesterday_info_deaths = yesterday_info_deaths if yesterday_info_deaths else 0
    yesterday_info_recovered = yesterday_info_recovered if yesterday_info_recovered else 0
    
    # absolute differences
    abs_diff_positive = today_info_positive - yesterday_info_positive
    abs_diff_deaths = today_info_deaths - yesterday_info_deaths
    abs_diff_recovered = today_info_recovered - yesterday_info_recovered

    # percentage differences
    perc_diff_positive = (today_info_positive / yesterday_info_positive - 1) if yesterday_info_positive != 0 else 0
    perc_diff_deaths = (today_info_deaths / yesterday_info_deaths - 1) if yesterday_info_deaths != 0 else 0
    perc_diff_recovered = (today_info_recovered / yesterday_info_recovered - 1) if yesterday_info_recovered != 0 else 0

    # plus or minus
    plus_positive = '+' if abs_diff_positive >=0 else ''
    plus_deaths = '+' if abs_diff_deaths >= 0 else ''
    plus_recovered = '+' if abs_diff_recovered >= 0 else ''

    # format into strings for print
    today_info_positive = f'{int(today_info_positive):,}'
    today_info_deaths = f'{int(today_info_deaths):,}'
    today_info_recovered = f'{int(today_info_recovered):,}'
    increase_info_positive = f'{plus_positive}{int(abs_diff_positive):,}, {perc_diff_positive:.1%}'
    increase_info_deaths = f'{plus_deaths}{int(abs_diff_deaths):,}, {perc_diff_deaths:.1%}'
    increase_info_recovered = f'{plus_recovered}{int(abs_diff_recovered):,}, {perc_diff_recovered:.1%}'

    return today_info_positive, increase_info_positive, \
        today_info_deaths, increase_info_deaths, \
        today_info_recovered, increase_info_recovered

# update overall stats display
@app.callback(
    [
        Output('graph-positive', 'figure'),
        Output('graph-deaths', 'figure'),
        Output('graph-recovered', 'figure')
    ],
    [Input('date-slider', 'value')]
)
def update_overall_graph_display(days_since_d1):
    #start = time.time()
    # graphs
    df_federal_until_today = DF_FEDERAL[DF_FEDERAL['Days Since First Case'] <= days_since_d1]
    fig_positive = px.line(
        df_federal_until_today,
        x = 'Date',
        y = 'Positive, Cumulative',
        template='plotly_white',
        color_discrete_map={'Positive, Cumulative':'Orange'},
        #width=150,
        height=100
    )
    #print(f'Time: {time.time() - start}')

    fig_deaths = px.line(
        df_federal_until_today,
        x = 'Date',
        y = 'Deaths, Cumulative',
        template='plotly_white',
        color_discrete_map={'Deaths, Cumulative':'Orange'},
        #width=150,
        height=100
    )

    fig_recovered = px.line(
        df_federal_until_today,
        x = 'Date',
        y = 'Recovered, Cumulative',
        template='plotly_white',
        color_discrete_map={'Recovered, Cumulative':'Orange'},
        #width=150,
        height=100
    )  
    
    fig_positive.update_xaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
    fig_positive.update_yaxes(showticklabels=False, visible=False, tickfont=dict(size=1))
    fig_deaths.update_xaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
    fig_deaths.update_yaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
    fig_recovered.update_xaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
    fig_recovered.update_yaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
    fig_positive.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig_deaths.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig_recovered.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig_positive, fig_deaths, fig_recovered

# update metric specific display 
@app.callback(
    [
        Output('metric-today-info', 'children'),
        Output('metric-info', 'children'),
        Output('metric-increase-info', 'children'),
    ],
    [
        Input('metric-select', 'value'),
        Input('date-slider', 'value')
    ]
)
def update_metric_display(metric, days_since_d1):
    # calculate information
    today_info_metric = sum(DF_FEDERAL[DF_FEDERAL['Days Since First Case'] == days_since_d1][metric])
    yesterday_info_metric = sum(DF_FEDERAL[DF_FEDERAL['Days Since First Case'] == (days_since_d1 -1)][metric])
    yesterday_info_metric = yesterday_info_metric if yesterday_info_metric else 0

    abs_diff_metric = today_info_metric - yesterday_info_metric
    perc_diff_metric = (today_info_metric / yesterday_info_metric - 1) if yesterday_info_metric != 0 else 0

    plus_metric = '+' if abs_diff_metric >=0 else ''

    # format for string printing
    today_info_metric = f'{int(today_info_metric):,}'
    increase_info_metric = f'{plus_metric}{int(abs_diff_metric):,}, {perc_diff_metric:.1%}'

    return today_info_metric, metric, increase_info_metric

@app.callback(
    Output('graph-metric', 'figure'),
    [
        Input('metric-select', 'value'),
        Input('date-slider', 'value')
    ]
)
def update_metric_graph(metric, days_since_d1):
    fig = px.line(
        DF_FEDERAL[DF_FEDERAL['Days Since First Case'] <= days_since_d1], 
        x = 'Date', 
        y = metric, 
        template = 'plotly_white',
        color_discrete_map = {metric: 'Orange'},
        #width=400,
        height=100
    )
    fig.update_xaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
    fig.update_yaxes(showticklabels=False, visible=False, tickfont=dict(size=1))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig