import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#444444'
}

# front-end
app.layout = html.Div(
    #style={'backgroundColor': colors['background']},
    children=[

        html.H1(
            children='COVIS-19',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.RadioItems(
            id='map-color-select',
            options=[
                {'label': 'Blue', 'value': 0},
                {'label': 'Red', 'value': 1},
            ],
            value=1
        ),

        dcc.Graph(id='map')

    ]
)

@app.callback(
    Output('map', 'figure'),
    [Input('map-color-select', 'value')]
)
def update_map_color(i):
    fig = px.choropleth(
        locationmode = 'USA-states',
        locations = ["CA", "TX", "NY"],
        color = [[1,2,3],[2,3,1]][i],
        scope = 'usa'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)