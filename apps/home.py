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
        html.H1(html.B('COVIS19 = COVID19 + DATAVIS')),
        #html.P(f"Last Updated {LATEST_DATE.strftime('%Y/%m/%d')}"),

        html.Div(
            className = 'row',
            children = [   
                html.Div(
                    className = 'six columns',
                    children = [
                        html.H4(children = 'Metric'),
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
                        html.H4(children = 'Date'),
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
        html.H4(children = 'Interactive Map'),
        dcc.Graph(id = 'map-interactive'),
        html.H4(children = 'Time Lapse Map'),
        dcc.Graph(id = 'map-time-lapse')
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
        color_continuous_scale = 'Inferno_r',
        height = 450
    )

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
        height = 600,
        animation_frame = 'Date',
        animation_group = metric,
        color_continuous_scale = 'Inferno_r'
    )
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
def update_metric_display(metric_name):
    metric_info = METRIC_DEFINITIONS[metric_name]
    return metric_name, metric_info