import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from data import *
from datetime import datetime, timedelta

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### DATA
URL = "https://covidtracking.com/api/v1/states/daily.json"
DF = dataframe_from_request(URL)
DF = clean_dataframe(DF)

# date variables
LATEST_DATE = max(DF['date'])
EARLIEST_DATE = min(DF['date'])
DELTA_DAYS = (LATEST_DATE - EARLIEST_DATE).days

### APP
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#444444'
}

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
    ])

### APP LAYOUT
app.layout = html.Div(
    #style={'backgroundColor': colors['background']},
    children=[

        html.H1(
            children='COVIS19',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.H4(
            children='covid19 + datavis = covis19',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.RadioItems(
            id = 'map-color-select',
            options = [
                {'label': 'Blue', 'value': 0},
                {'label': 'Red', 'value': 1},
            ],
            value = 1
        ),

        html.Div(
            id = 'date-slider-output',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.Slider(
            id = 'date-slider',
            min = 0,
            max = DELTA_DAYS,
            marks = {i:(EARLIEST_DATE + timedelta(days=i)).strftime('%Y/%m/%d') \
                for i in range(int(DELTA_DAYS/10), DELTA_DAYS-int(DELTA_DAYS/10), int(DELTA_DAYS/5))},
            value = DELTA_DAYS
        ),

        dcc.Graph(id = 'map'),

        generate_table(DF)

    ]
)

### APP CALLBACKS
@app.callback(
    Output('map', 'figure'),
    [Input('date-slider', 'value')]
)
def update_map_color(i):
    fig = px.choropleth(
        #DF[DF['date'] == EARLIEST_DATE + timedelta(days=i)],
        DF.sort_values(by=['date']),
        # dynamic
        color = 'positive',
        locations = 'state',
        range_color = (0, max(DF['positive'])),
        # static
        locationmode = 'USA-states',
        scope = 'usa',
        height = 600,
        animation_frame = 'dateString',
        animation_group = 'positive',
        color_continuous_scale = 'Inferno_r'
    )
    return fig

@app.callback(
    dash.dependencies.Output('date-slider-output', 'children'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_output(i):
    return (EARLIEST_DATE + timedelta(days=i)).strftime('%Y/%m/%d')

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)