import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from app import app, server
from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format, Sign
import dash_table.FormatTemplate as FormatTemplate

from datetime import datetime, timedelta

from data.finance import DF, EARLIEST_DATE, LATEST_DATE, DELTA_DAYS

'''
da = DF.to_dict('records')
cols = [{'name': i, 'id': i} for i in DF.columns]
output = dash_table.DataTable(
    columns = cols,
    data = da,
    sort_action='native',
    filter_action='native',
    style_cell={'fontSize':15, 'font-family':'sans-serif', 'textAlign': 'left'},
    style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},
    style_as_list_view=True,
)
'''
@app.callback(
    Output('graph', 'figure'),
    [Input('date-slider', 'value')]
)
def FAANG_graph(days_since_ny):
    data = DF[DF['Days Since NY'] <= days_since_ny]
    latest_day = max((data['Date']))
    fig = px.line(
        data,
        x='Date',
        y='% Diff YTD',
        color='Stock',
        color_discrete_sequence = px.colors.qualitative.T10,
        template = 'plotly_white',
        height = 600
    )
    fig.update_layout(legend_orientation="h", legend=dict(x=-.1, y=1.1))
    for i, row in data[data['Date'] == latest_day].iterrows():
        plus = '+' if row['% Diff YTD'] >= 0 else ''
        fig.add_annotation(x=row['Date'], y=row['% Diff YTD'], text=f"{row['Stock']} {plus}{round(row['% Diff YTD'], 1)}%")
    
    if latest_day >= datetime.strptime('2020-01-21', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-01-21', y0=min(data['% Diff YTD']), x1='2020-01-21', y1=max(data['% Diff YTD']), 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-01-21', y=max(data['% Diff YTD'])+1, text='01/21 - 1st US COV19 Case')

    if latest_day >= datetime.strptime('2020-02-19', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-02-19', y0=min(data['% Diff YTD']), x1='2020-02-19', y1=max(data['% Diff YTD']), 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-02-19', y=max(data['% Diff YTD'])+1, text='02/19 - Mkt Record High')

    if latest_day >= datetime.strptime('2020-02-28', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-02-28', y0=min(data['% Diff YTD']), x1='2020-02-28', y1=max(data['% Diff YTD'])-2, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-02-28', y=max(data['% Diff YTD'])-1, text='02/28 - Mkt Correction (-10%)')

    if latest_day >= datetime.strptime('2020-03-09', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-03-09', y0=min(data['% Diff YTD']), x1='2020-03-09', y1=max(data['% Diff YTD'])-4, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-03-09', y=max(data['% Diff YTD'])-3, text='03/09 - Bear Mrt (-20%)')

    fig.update_annotations(dict(xref="x", yref="y", showarrow=True, arrowhead=7, ax=60, ay=0))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=True, zerolinewidth=0.05, zerolinecolor='Gray')
    return fig

child = [
    # navigation bar
    html.Ul(
        className = 'topnav',
        children = [
            html.Li(html.A(html.B('COVIS19'), className = 'active', href='/')),
            html.Li(html.A('💊Health', href='/')),
            html.Li(html.A('💵Finance', className = 'active', href='#')),
            #html.Li(html.A('About', href='/about')),
            html.Li(className = 'right', children=[html.A('💻Github', href='https://github.com/jiecai1997/covis19')])
        ]
    ),
    dcc.Slider(
        id = 'date-slider',
        min = 0,
        max = DELTA_DAYS,
        marks = {i:(EARLIEST_DATE + timedelta(days=i)).strftime('%Y/%m/%d') \
            for i in range(int(DELTA_DAYS/8), (DELTA_DAYS+1-int(DELTA_DAYS/8)), int(DELTA_DAYS/4))},
        value = DELTA_DAYS
    ),
    dcc.Loading(dcc.Graph(id = 'graph'), color = '#222222', type = 'circle')
    #html.Div(output)
]

layout = html.Div(
    className = 'container',
    children = child
)
