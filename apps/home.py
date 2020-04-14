import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import *
from app import app
from dash.dependencies import Input, Output

colors = {
    'background': '#FFFFFF',
    'text': '#444444'
}

my_style = {
    'textAlign': 'center',
    'color': colors['text']
}

### FUNCTIONS
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
        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'four columns',
                    children = [
                        html.H2(html.Strong(id = 'stats-today-info-positive')),
                        html.Strong('Positive, Cumulative'),
                        html.P(id = 'stats-increase-info-positive')
                    ]
                ),
                html.Div(
                    className = 'four columns',
                    children = [
                        html.H2(html.Strong(id = 'stats-today-info-deaths')),
                        html.Strong('Deaths, Cumulative'),
                        html.P(id = 'stats-increase-info-deaths')
                    ]
                ),
                html.Div(
                    className = 'four columns',
                    children = [
                        html.H2(html.Strong(id = 'stats-today-info-recovered')),
                        html.Strong('Recoverd, Cumulative'),
                        html.P(id = 'stats-increase-info-recovered')
                    ]
                )
            ]
        ),
        html.Hr(),
        html.Div(
            className = 'row',
            children = [   
                html.Div(
                    className = 'six columns',
                    children = [
                        html.H5(children = 'Metric'),
                        dcc.Dropdown(
                            id = 'metric-select',
                            options = METRIC_SELECT_OPTIONS,
                            value = 'Positive, Cumulative'
                        ),  
                        html.Br(),
                        html.Strong(id = 'metric-name-output'),
                        html.P(id = 'metric-info-output'),            
                    ]
                ),
                html.Div(
                    className = 'six columns',
                    children = [
                        html.H5(children = 'Date'),
                        dcc.Slider(
                            id = 'date-slider',
                            min = 0,
                            max = DELTA_DAYS,
                            marks = {i:(EARLIEST_DATE + timedelta(days=i)).strftime('%Y/%m/%d') \
                                for i in range(int(DELTA_DAYS/8), DELTA_DAYS-int(DELTA_DAYS/8), int(DELTA_DAYS/4))},
                            value = DELTA_DAYS
                        ),
                        html.Br(),
                        html.Strong(id = 'date-output'),
                        html.P(id = 'days-since-d1-output'),
                    ]
                )
            ]
        ),
        html.Hr(),
        dcc.Graph(id = 'overall-stats-graph'),
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
        #generate_table(DF)
    ]
)

### APP CALLBACKS
# update map
@app.callback(
    [
        Output('map-interactive', 'figure'),
        Output('map-time-lapse', 'figure')
    ],
    [
        Input('date-slider', 'value'),
        Input('metric-select', 'value')
    ]
)
def update_maps(days_since_d1, metric):

    # map without animation
    map_interactive = px.choropleth(
        DF[DF['date'] == EARLIEST_DATE + timedelta(days=days_since_d1)],

        # dynamic
        color = metric,
        locations = 'State',
        range_color = (0, max(DF[metric])),

        # static
        locationmode = 'USA-states',
        scope = 'usa',
        color_continuous_scale = 'Oranges',
        height = 450
    )
    map_interactive.update_layout(showlegend=False)

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
    map_time_lapse.update_layout(showlegend=False)
    return map_interactive, map_time_lapse

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
def update_overall_stats_display(days_since_d1):
    # calculate metrics
    # current day's info
    today_info_positive = sum(DF[DF['Days Since First Case'] == days_since_d1]['Positive, Cumulative'])   
    today_info_deaths = sum(DF[DF['Days Since First Case'] == days_since_d1]['Deaths, Cumulative'])
    today_info_recovered = sum(DF[DF['Days Since First Case'] == days_since_d1]['Recovered, Cumulative'])

    # previous day's info
    yesterday_info_positive = sum(DF[DF['Days Since First Case'] == (days_since_d1 -1)]['Positive, Cumulative'])
    yesterday_info_deaths = sum(DF[DF['Days Since First Case'] == (days_since_d1 -1)]['Deaths, Cumulative'])
    yesterday_info_recovered = sum(DF[DF['Days Since First Case'] == (days_since_d1 -1)]['Recovered, Cumulative'])
    
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

    # format into strings for print
    today_info_positive = f'{int(today_info_positive):,}'
    today_info_deaths = f'{int(today_info_deaths):,}'
    today_info_recovered = f'{int(today_info_recovered):,}'
    increase_info_positive = f'{int(abs_diff_positive):,}, {perc_diff_positive:.1%}'
    increase_info_deaths = f'{int(abs_diff_deaths):,}, {perc_diff_deaths:.1%}'
    increase_info_recovered = f'{int(abs_diff_recovered):,}, {perc_diff_recovered:.1%}'

    return today_info_positive, increase_info_positive, \
        today_info_deaths, increase_info_deaths, \
        today_info_recovered, increase_info_recovered

# TODO update metric specific display 
@app.callback(
    [
        Output('stats-today-info', 'children'),
        Output('stats-increase-info', 'children'),
    ],
    [
        Input('metric-select', 'value'),
        Input('date-slider', 'value')
    ]
)
def update_metric_specific_display(metric, days_since_d1):
    '''
    df_overall = DF[DF['Days Since First Case'] < days_since_d1].groupby('Date')[metric].agg('sum').reset_index()
    fig = px.bar(
        df_overall, 
        x = 'Date', 
        y = metric, 
        template = 'plotly_white',
        color_discrete_map = {metric: 'Orange'}
    )
    '''

    # calculate information
    today_info = sum(DF[DF['Days Since First Case'] == days_since_d1][metric])
    yesterday_info = sum(DF[DF['Days Since First Case'] == max((days_since_d1 -1), 0)][metric])
    abs_increase = today_info - yesterday_info
    if yesterday_info == 0:
        perc_increase = None
    else:
        perc_increase = round((today_info / yesterday_info - 1)*100, 1)
    plus = None
    if abs_increase >= 0 and perc_increase >= 0:
        plus = '+'

    # format for string printing
    today_info = f'{int(today_info):,}'
    if days_since_d1 == 0:
        increase_info = '-'
    if plus is None:
        increase_info = f'{int(abs_increase):,}, {perc_increase}%'
    else:
        increase_info = f'{plus}{int(abs_increase):,}, {perc_increase}%'
    return today_info, increase_info