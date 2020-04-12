import dash_core_components as dcc
import dash_html_components as html
from app import app

colors = {
    'background': '#FFFFFF',
    'text': '#444444'
}

layout = html.Div(
    children=[

        html.Nav(
            children = [
                dcc.Link('Home', href='/'),
                dcc.Link('About', href='#'),
                html.A('Github', href='https://github.com/jiecai1997/covis19')
            ],
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.H1(
            children = 'about',
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        
    ]
)