import dash_core_components as dcc
import dash_html_components as html
from app import app

colors = {
    'background': '#FFFFFF',
    'text': '#444444'
}

layout = html.Div(
    className = 'container',
    children=[
        html.Ul(
            className = 'topnav',
            children = [
                html.Li(html.A(html.B('COVIS19'), href='/')),
                html.Li(html.A('About', className = 'active', href='#')),
                html.Li(className = 'right', children=[html.A('Github', href='https://github.com/jiecai1997/covis19')])
            ]
        ),
        html.Br(),
        html.H1(html.B('COVIS19 = COVID19 + DATAVIS')) 
    ]
)