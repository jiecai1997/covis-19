import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from app import app, server
from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format, Sign
import dash_table.FormatTemplate as FormatTemplate

from datetime import datetime, timedelta
import math

from data.finance import DF, EARLIEST_DATE, LATEST_DATE, DELTA_DAYS
from const import INDEXES, FAANGM, TICKERS

### HELPER FUNCTIONS
def subset_data(df, category):
    return df[df['Stock'].isin(category)]

def ticker_info(days_since_ny, ticker):
    #print('ticker info', ticker)
    data = DF[(DF['Days Since NY'] == days_since_ny) & (DF['Stock'] == ticker)]
    price_current = data['Close'].iloc[0]
    price_delta_ytd = data['$ Delta YTD'].iloc[0]
    perc_delta_ytd = data['% Delta YTD'].iloc[0]
    plus = '+' if price_delta_ytd >= 0 else ''
    output_price_current = f'${price_current:.2f}'
    output_delta_ytd = f'YTD | {plus}${price_delta_ytd:.2f}, {plus}{perc_delta_ytd:.1f}%'
    return output_price_current, output_delta_ytd
        
def industry_overall_view(industry):
    tt = list(industry.keys())
    div = []
    for i in range(int(len(industry)/3)):
        ticker1, ticker2, ticker3 = tt[3*i], tt[3*i+1], tt[3*i+2]
        new_div = html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'two columns',
                    children = [
                        html.H2(html.Strong(id=f'{ticker1}-current')),
                        html.Strong(f'{industry[ticker1]} ({ticker1})'), 
                        html.Div(id = f'{ticker1}-ytd'),
                        html.Br() 
                    ]
                ),
                html.Div(
                    className = 'two columns',
                    children = 'placeholder'#dcc.Loading(dcc.Graph(id = f'{state1}-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [
                        html.H2(html.Strong(id=f'{ticker2}-current')),
                        html.Strong(f'{industry[ticker2]} ({ticker2})'),
                        html.Div(id = f'{ticker2}-ytd'),
                        html.Br() 
                    ]
                ),
                html.Div(
                    className = 'two columns',
                    children = 'placeholder'#dcc.Loading(dcc.Graph(id = f'{state2}-metric-graph', style = gh), color = '#222222', type = 'circle')
                ),
                html.Div(
                    className = 'two columns',
                    children = [
                        html.H2(html.Strong(id=f'{ticker3}-current')),
                        html.Strong(f'{industry[ticker3]} ({ticker3})'), 
                        html.Div(id = f'{ticker3}-ytd'),
                        html.Br() 
                    ]
                ),
                html.Div(
                    className = 'two columns',
                    children = 'placeholder'#dcc.Loading(dcc.Graph(id = f'{state3}-metric-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),
        div.append(new_div)
    div = [item for sublist in div for item in sublist]
    return div

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
    html.Br(),
    html.P(
        children = ['💵',html.A('Source', href = 'https://github.com/ranaroussi/yfinance'),
        ' updated ', LATEST_DATE.strftime('%Y/%m/%d'),
        ', US market only']
    ),
    html.Br(),
    html.H5('Date'),
    html.Strong(id = 'date-print'),
    html.P(id='ytd-print'),
    dcc.Slider(
        id = 'date-slider',
        min = 0,
        max = DELTA_DAYS,
        marks = {i:(EARLIEST_DATE + timedelta(days=i)).strftime('%Y/%m/%d') \
            for i in range(int(DELTA_DAYS/8), (DELTA_DAYS+1-int(DELTA_DAYS/8)), int(DELTA_DAYS/4))},
        value = DELTA_DAYS
    ),
    html.Hr(),
    html.H5('Key Indexes'),
    html.Div(industry_overall_view(INDEXES)),
    html.Br(),
    html.H5('FAANG + Microsoft'),
    html.Div(industry_overall_view(FAANGM)),
    html.Br(),
    html.H5('Airlines'),
    html.Br(),
    dcc.Loading(dcc.Graph(id = 'graph'), color = '#222222', type = 'circle')
    #html.Div(output)
]

### MAIN LAYOUT
layout = html.Div(
    className = 'container',
    children = child
)

### CALLBACKS
##### date display
@app.callback(
    [Output('date-print', 'children'), Output('ytd-print', 'children')],
    [Input('date-slider', 'value')]
)
def update_dates_display(days_since_d1):
    date_output = f'{(EARLIEST_DATE + timedelta(days=days_since_d1)).strftime("%Y/%m/%d")}'
    days_since_d1_output = f'{days_since_d1} day(s) YTD since 2020-01-01.'
    return date_output, days_since_d1_output

def a(ticker):
    @app.callback(
        [Output(f'{ticker}-current', 'children'), Output(f'{ticker}-ytd', 'children')],
        [Input('date-slider', 'value')]
    )
    def return_ticker_info(days_since_ny):
        print('inner loop callback', ticker) # broken here [4,4,4,4]
        return ticker_info(days_since_ny = days_since_ny, ticker = ticker)

for ticker in list(TICKERS.keys()):
    print('outer loop callback', ticker) # fine here [1,2,3,4]
    a(ticker)

##### graph
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
        y='% Delta YTD',
        color='Stock',
        color_discrete_sequence = px.colors.qualitative.T10,
        hover_name = 'Stock',
        hover_data=['$ Delta YTD', 'Close'],
        template = 'plotly_white',
        height = 600
    )
    fig.update_layout(legend_orientation="h", legend=dict(x=-.1, y=1.1))
    for i, row in data[data['Date'] == latest_day].iterrows():
        plus = '+' if row['% Delta YTD'] >= 0 else ''
        fig.add_annotation(x=row['Date'], y=row['% Delta YTD'], text=f"{row['Stock']} {plus}{round(row['% Delta YTD'], 1)}%")
    
    if latest_day >= datetime.strptime('2020-01-21', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-01-21', y0=min(data['% Delta YTD']), x1='2020-01-21', y1=max(data['% Delta YTD'])+3, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-01-21', y=max(data['% Delta YTD'])+4, text='01/21 - 1st US COVID-19 Case')

    if latest_day >= datetime.strptime('2020-02-19', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-02-19', y0=min(data['% Delta YTD']), x1='2020-02-19', y1=max(data['% Delta YTD'])+1, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-02-19', y=max(data['% Delta YTD'])+2, text='02/19 - Market Record High')

    if latest_day >= datetime.strptime('2020-02-28', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-02-28', y0=min(data['% Delta YTD']), x1='2020-02-28', y1=max(data['% Delta YTD'])-3, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-02-28', y=max(data['% Delta YTD']), text='02/28 - 1st US COVID-19 Death')
        fig.add_annotation(x='2020-02-28', y=max(data['% Delta YTD'])-2, text='02/28 - Market Correction (-10%)')

    if latest_day >= datetime.strptime('2020-03-09', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-03-09', y0=min(data['% Delta YTD']), x1='2020-03-09', y1=max(data['% Delta YTD'])-5, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-03-09', y=max(data['% Delta YTD'])-4, text='03/09 - Bear Market (-20%)')

    fig.update_annotations(dict(xref="x", yref="y", showarrow=True, arrowhead=7, ax=60, ay=0))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=True, zerolinewidth=0.05, zerolinecolor='Gray')
    return fig