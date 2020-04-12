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

### FUNCTIONS
def generate_table(dataframe, max_rows=10):
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
    #style={'backgroundColor': colors['background']},
    children=[

        html.Nav(
            children = [
                dcc.Link('Home', href='#'),
                dcc.Link('About', href='/about'),
                html.A('Github', href='https://github.com/jiecai1997/covis19')
            ],
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.H1(
            children = 'COVIS19',
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Hr(),

        html.H3(
            id = 'date-output',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(
            id = 'days-since-d1-output',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Br(),

        dcc.Slider(
            id = 'date-slider',
            min = 0,
            max = DELTA_DAYS,
            marks = {i:(EARLIEST_DATE + timedelta(days=i)).strftime('%Y/%m/%d') \
                for i in range(int(DELTA_DAYS/10), DELTA_DAYS-int(DELTA_DAYS/10), int(DELTA_DAYS/5))},
            value = DELTA_DAYS
        ),

        dcc.RadioItems(
            id = 'metric-select',
            options = [
                {'label': 'Positive, Cumulative', 'value': 'positive'},
                {'label': 'Negative, Cumulative', 'value': 'negative'},
            ],
            value = 'positive'
        ),

        dcc.Graph(id = 'map'),

        generate_table(DF)
    ]
)

### APP CALLBACKS
# update map
@app.callback(
    Output('map', 'figure'),
    [
        Input('date-slider', 'value'),
        Input('metric-select', 'value')
    ]
)
def update_map(days_since_d1, metric):
    '''
    # map with animation
    # cool but missing a lot of capabilities
    fig = px.choropleth(
        #DF[DF['date'] == EARLIEST_DATE + timedelta(days=i)],
        DF.sort_values(by=['date']),

        # dynamic
        color = metric,
        locations = 'state',
        range_color = (0, max(DF[metric])),

        # static
        locationmode = 'USA-states',
        scope = 'usa',
        height = 600,
        animation_frame = 'dateString',
        animation_group = metric,
        color_continuous_scale = 'Inferno_r'
    )
    '''

    # map without animation
    fig = px.choropleth(
        DF[DF['date'] == EARLIEST_DATE + timedelta(days=days_since_d1)],

        # dynamic
        color = metric,
        locations = 'state',
        range_color = (0, max(DF[metric])),

        # static
        locationmode = 'USA-states',
        scope = 'usa',
        height = 500,
        color_continuous_scale = 'Inferno_r'
    )
    return fig

# update date display
@app.callback(
    [
        Output('date-output', 'children'),
        Output('days-since-d1-output', 'children')
    ],
    [Input('date-slider', 'value')])
def update_dates_days_output(days_since_d1):
    date_output = f'{(EARLIEST_DATE + timedelta(days=days_since_d1)).strftime("%Y/%m/%d")}'
    days_since_d1_output = f'{days_since_d1} Days Since First US Case'
    return date_output, days_since_d1_output