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
import yfinance as yf

from data.finance import DF, EARLIEST_DATE, LATEST_DATE, DELTA_DAYS
from const import INDICES, FAANGM, AIRLINES, TICKERS

gh = {'height': '120px'}

### HELPER FUNCTIONS
def subset_data(df, category):
    return df[df['Stock'].isin(category)]

def ytd_delta_output(price_delta, perc_delta):
    plus_price = '+' if price_delta >= 0 else '-'
    plus_perc = '+' if perc_delta >= 0 else ''
    return (f'YTD | {plus_price}${abs(price_delta):.2f}, {plus_perc}{perc_delta:.1f}%')
        
def industry_overall_view(industry):
    tickers = list(industry.keys())
    tickers_str_id = tickers[0]
    div = []
    for i in range(int(len(industry)/3)):
        ticker1, ticker2, ticker3 = tickers[3*i], tickers[3*i+1], tickers[3*i+2]
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
                    children = dcc.Loading(dcc.Graph(id = f'{ticker1}-graph', style = gh), color = '#222222', type = 'circle')
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
                    children = dcc.Loading(dcc.Graph(id = f'{ticker2}-graph', style = gh), color = '#222222', type = 'circle')
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
                    children = dcc.Loading(dcc.Graph(id = f'{ticker3}-graph', style = gh), color = '#222222', type = 'circle')
                )
            ]
        ),
        div.append(new_div)
    br = html.Br(),
    div.append(br)
    div.append(br)
    industry_graph = dcc.Loading(dcc.Graph(id = f'{tickers_str_id}-industry-graph'), color = '#222222', type = 'circle'),
    div.append(industry_graph)
    div = [item for sublist in div for item in sublist]
    return div

### CALLBACKS
##### date display
@app.callback(
    [Output('date-print', 'children'), Output('ytd-print', 'children')],
    [Input('date-slider', 'value')]
)
def update_dates_display(days_since_d1):
    date_output = f'{(EARLIEST_DATE + timedelta(days=days_since_d1)).strftime("%Y/%m/%d")}'
    days_since_d1_output = f'{days_since_d1} day(s) YTD.'
    return date_output, days_since_d1_output

def ticker_display(ticker):
    # ticker price and delta info
    @app.callback(
        [Output(f'{ticker}-current', 'children'), Output(f'{ticker}-ytd', 'children')],
        [Input('date-slider', 'value')]
    )
    def ticker_info(days_since_ny):
        data = DF[(DF['Days Since NY'] <= days_since_ny) & (DF['Stock'] == ticker)]
        data = data[data['Days Since NY'] == max(data['Days Since NY'])]
        price_current = data['Close'].iloc[0]
        price_delta = data['$ Delta YTD'].iloc[0]
        perc_delta = data['% Delta YTD'].iloc[0]
        output_delta = ytd_delta_output(price_delta, perc_delta)
        output_price_current = f'${price_current:.2f}'
        return output_price_current, output_delta

    # ticker graph
    @app.callback(
        Output(f'{ticker}-graph', 'figure'),
        [Input('date-slider', 'value')]
    )
    def ticker_graph(days_since_ny):
        data = DF[(DF['Days Since NY'] <= days_since_ny) & (DF['Stock'] == ticker)]
        latest_price = data[data['Date'] == max(data['Date'])]['Close'].iloc[0]
        earliest_price = data[data['Date'] == min(data['Date'])]['Close'].iloc[0]
        fig = px.line(
            data,
            x='Date',
            y='% Delta YTD',
            hover_name = 'Company',
            hover_data=['$ Delta YTD', 'Close', 'Stock'],
            color_discrete_sequence= ['#54A24B'] if latest_price >= earliest_price else ['#E45756'],
            template = 'plotly_white',
            height = 120
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        fig.update_xaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
        fig.update_yaxes(showticklabels=False, visible=False, tickfont=dict(size=1))
        return fig

for ticker in list(TICKERS.keys()):
    ticker_display(ticker)

#### industry graph
def industry_graph_display(industry):
    industry_str_id = list(industry.keys())[0]
    @app.callback(
        Output(f'{industry_str_id}-industry-graph', 'figure'),
        [Input('date-slider', 'value')]
    )
    def industry_graph(days_since_ny):
        data = DF[(DF['Days Since NY'] <= days_since_ny) & (DF['Stock'].isin(industry.keys()))]
        latest_day = max((data['Date']))
        fig = px.line(
            data,
            x='Date',
            y='% Delta YTD',
            color='Stock',
            color_discrete_sequence = px.colors.qualitative.Antique,
            hover_name = 'Company',
            hover_data=['$ Delta YTD', 'Close', 'Stock'],
            template = 'plotly_white',
            height = 600
        )
        fig.update_layout(legend_orientation="h", legend=dict(x=-.1, y=1.1))
        y_min = min(data['% Delta YTD'])
        y_max = max(data['% Delta YTD'])
        y_diff_scale = (y_max - y_min)/25
        for i, row in data[data['Date'] == latest_day].iterrows():
            plus = '+' if row['% Delta YTD'] >= 0 else ''
            fig.add_annotation(x=row['Date'], y=row['% Delta YTD'], text=f"{row['Stock']} {plus}{round(row['% Delta YTD'], 1)}%")
        
        if latest_day >= datetime.strptime('2020-01-21', '%Y-%m-%d'):
            fig.add_shape(dict(type="line", x0='2020-01-21', y0=min(data['% Delta YTD']), x1='2020-01-21', y1=max(data['% Delta YTD'])+1.5*y_diff_scale, 
                            line=dict(color='Black', width=0.1, dash="dot")))
            fig.add_annotation(x='2020-01-21', y=max(data['% Delta YTD'])+2*y_diff_scale, text='01/21 - 1st US COVID-19 Case')

        if latest_day >= datetime.strptime('2020-02-19', '%Y-%m-%d'):
            fig.add_shape(dict(type="line", x0='2020-02-19', y0=min(data['% Delta YTD']), x1='2020-02-19', y1=max(data['% Delta YTD'])+1.5*y_diff_scale, 
                            line=dict(color='Black', width=0.1, dash="dot")))
            fig.add_annotation(x='2020-02-19', y=max(data['% Delta YTD'])+2*y_diff_scale, text='02/19 - Market Record High')

        if latest_day >= datetime.strptime('2020-02-28', '%Y-%m-%d'):
            fig.add_shape(dict(type="line", x0='2020-02-28', y0=min(data['% Delta YTD']), x1='2020-02-28', y1=max(data['% Delta YTD'])-.5*y_diff_scale, 
                            line=dict(color='Black', width=0.1, dash="dot")))
            fig.add_annotation(x='2020-02-28', y=max(data['% Delta YTD'])+y_diff_scale, text='02/28 - 1st US COVID-19 Death')
            fig.add_annotation(x='2020-02-28', y=max(data['% Delta YTD']), text='02/28 - Market Correction (-10%)')

        if latest_day >= datetime.strptime('2020-03-09', '%Y-%m-%d'):
            fig.add_shape(dict(type="line", x0='2020-03-09', y0=min(data['% Delta YTD']), x1='2020-03-09', y1=max(data['% Delta YTD'])-1.5*y_diff_scale, 
                            line=dict(color='Black', width=0.1, dash="dot")))
            fig.add_annotation(x='2020-03-09', y=max(data['% Delta YTD'])-y_diff_scale, text='03/09 - Bear Market (-20%)')

        fig.update_annotations(dict(xref="x", yref="y", showarrow=True, arrowhead=7, ax=60, ay=0))
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, zeroline=True, zerolinewidth=0.05, zerolinecolor='Gray')
        return fig

for industry in [INDICES, FAANGM, AIRLINES]:
    industry_graph_display(industry)

def custom_stock_df(ticker):
    df = yf.download(str.upper(ticker), start='2020-01-01').reset_index()
    if not df.empty:
        #name = yf.Ticker(ticker).info['shortName'].split()
        #name = ' '.join(name[:2]) if len(name) > 3 else name[0]
        df['Stock'] = ticker
        df['Company'] = ticker
        initial = df[df['Date'] == min(df['Date'])]['Close'][0]
        df['$ Delta YTD'] = (df['Close'] - initial)
        df['% Delta YTD'] = ((df['Close'] - initial)/initial)*100
        df['Days Since NY'] = df['Date'].apply(lambda x: (x - EARLIEST_DATE).days)
        df = df.round({'Open': 2, 'High': 2, 'Low':2, 'Close':2, 'Adj Close':2, '$ Delta YTD':2, '% Delta YTD':1})
    return df

def custom_stock_info(ticker):
    '''
    name = yf.Ticker(ticker).info['shortName']
    if ' ' in name:
        name = name.split()
        name = ' '.join(name[:2]) if len(name) > 3 else name[0]
    '''
    return f'{str.upper(ticker)}'

# custom stock vs market
@app.callback(
    Output('custom-stock-info', 'children'),
    [Input('custom-stock-input', 'value'), Input('date-slider', 'value')]
)
def custom_stock_output(ticker, days_since_ny):
    df = custom_stock_df(ticker)
    if df.empty:
        return 'Invalid Stock Ticker'
    else:
        return custom_stock_info(ticker)

@app.callback(
    [
        Output('custom-stock-price', 'children'),
        Output('custom-stock-info-2', 'children'),
        Output('custom-stock-ytd', 'children')
    ],
    [Input('custom-stock-input', 'value'), Input('date-slider', 'value')]
)
def custom_stock_price(ticker, days_since_ny):
    df = custom_stock_df(ticker)
    if df.empty:
        return '-', 'Invalid Stock Ticker', '-'
    else:
        info = custom_stock_info(ticker)
        data = df[df['Days Since NY'] <= days_since_ny]
        df_today = data[data['Days Since NY'] == max(data['Days Since NY'])]
        price = df_today['Close'].iloc[0]
        output_price = f'${price:.2f}'
        price_delta = df_today['$ Delta YTD'].iloc[0]
        perc_delta = df_today['% Delta YTD'].iloc[0]
        output_delta = ytd_delta_output(price_delta, perc_delta)
        return output_price, info, output_delta

@app.callback(
    Output('custom-stock-graph', 'figure'),
    [Input('custom-stock-input', 'value'), Input('date-slider', 'value')]
)
def custom_stock_graph(ticker, days_since_ny):
    data = custom_stock_df(ticker)
    data = data[data['Days Since NY'] <= days_since_ny]
    if data.empty:
        fig = px.line(
            [[0,0], [1,1]],
            template = 'plotly_white',
            height = 120
        )
    else:
        latest_price = data[data['Days Since NY'] == max(data['Days Since NY'])]['Close'].iloc[0]
        earliest_price = data[data['Days Since NY'] == min(data['Days Since NY'])]['Close'].iloc[0]
        fig = px.line(
            data,
            x='Date',
            y='% Delta YTD',
            hover_name = 'Company',
            hover_data=['$ Delta YTD', 'Close', 'Stock'],
            color_discrete_sequence= ['#54A24B'] if latest_price >= earliest_price else ['#E45756'],
            template = 'plotly_white',
            height = 120
        )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_xaxes(showticklabels=False, visible = False, tickfont=dict(size=1))
    fig.update_yaxes(showticklabels=False, visible=False, tickfont=dict(size=1))
    return fig

# index display vs custom
def ticker_display_custom(ticker):
    # ticker price and delta info
    @app.callback(
        [Output(f'{ticker}-info-custom', 'children'), Output(f'{ticker}-ytd-custom', 'children')],
        [Input('date-slider', 'value')]
    )
    def ticker_info(days_since_ny):
        name = INDICES[ticker]
        data = DF[(DF['Days Since NY'] <= days_since_ny) & (DF['Stock'] == ticker)]
        data = data[data['Days Since NY'] == max(data['Days Since NY'])]
        price_delta = data['$ Delta YTD'].iloc[0]
        perc_delta = data['% Delta YTD'].iloc[0]
        output_delta = ytd_delta_output(price_delta, perc_delta)
        info = f'{name} ({ticker})'
        return info, output_delta

for ticker in INDICES.keys():
    ticker_display_custom(ticker)

# custom vs index result
@app.callback(
    Output('custom-vs-market-result', 'children'),
    [Input('custom-stock-input', 'value'), Input('date-slider', 'value')]
)
def custom_vs_market_result(ticker, days_since_ny):
    df = custom_stock_df(ticker)
    df = df[df['Days Since NY'] <= days_since_ny]
    DF_TEMP = DF[DF['Days Since NY'] <= days_since_ny]
    if df.empty:
        return '🤷🏻‍♀️Invalid Stock Ticker'
    
    custom_perc_delta = df[df['Days Since NY'] == max(df['Days Since NY'])]['% Delta YTD'].iloc[0]
    nasdaq_perc_delta = DF_TEMP[(DF_TEMP['Days Since NY'] == max(DF_TEMP['Days Since NY'])) & (DF_TEMP['Stock'] == '^IXIC')]['% Delta YTD'].iloc[0]
    sp500_perc_delta = DF_TEMP[(DF_TEMP['Days Since NY'] == max(DF_TEMP['Days Since NY'])) & (DF_TEMP['Stock'] == '^GSPC')]['% Delta YTD'].iloc[0]
    dow_perc_delta = DF_TEMP[(DF_TEMP['Days Since NY'] == max(DF_TEMP['Days Since NY'])) & (DF_TEMP['Stock'] == '^DJI')]['% Delta YTD'].iloc[0]

    if custom_perc_delta > max(nasdaq_perc_delta, sp500_perc_delta, dow_perc_delta):
        return f'{str.upper(ticker)} = 👍Better Than Market Average'
    elif custom_perc_delta < min(nasdaq_perc_delta, sp500_perc_delta, dow_perc_delta):
        return f'{str.upper(ticker)} = 👎Worse Than Market Average'
    else:
        return f'{str.upper(ticker)} = 🤷🏻‍♀️Around Market Average'

# custom vs index compare graph
@app.callback(
    Output('custom-vs-market-graph', 'figure'),
    [Input('custom-stock-input', 'value'), Input('date-slider', 'value')]
)
def custom_vs_market_graph(ticker, days_since_ny):
    df = custom_stock_df(ticker)
    df['Highlight'] = 1
    df2 = DF[DF['Stock'].isin(INDICES)]
    df2['Highlight'] = 0
    data = df.append(df2)
    data = data[data['Days Since NY'] <= days_since_ny]
    dd = df[df['Days Since NY'] <= days_since_ny]
    latest_price = dd[dd['Days Since NY'] == max(dd['Days Since NY'])]['Close'].iloc[0]
    earliest_price = df[df['Days Since NY'] == min(df['Days Since NY'])]['Close'].iloc[0]
    fig = px.line(
        data,
        x='Date',
        y='% Delta YTD',
        color='Highlight',
        line_group = 'Stock',
        color_discrete_sequence = ['#E2E2E2', '#54A24B'] if latest_price >= earliest_price else ['#E2E2E2', '#E45756'],
        category_orders={'Highlight': [0, 1]},
        hover_name = 'Company',
        hover_data=['$ Delta YTD', 'Close', 'Stock'],
        template = 'plotly_white',
        height = 600
    )
    fig.update_layout(showlegend=False)
    latest_day = max((data['Date']))
    y_min = min(data['% Delta YTD'])
    y_max = max(data['% Delta YTD'])
    y_diff_scale = (y_max - y_min)/25
    for i, row in data[data['Date'] == latest_day].iterrows():
        plus = '+' if row['% Delta YTD'] >= 0 else ''
        fig.add_annotation(x=row['Date'], y=row['% Delta YTD'], text=f"{row['Stock']} {plus}{round(row['% Delta YTD'], 1)}%")
    
    if latest_day >= datetime.strptime('2020-01-21', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-01-21', y0=min(data['% Delta YTD']), x1='2020-01-21', y1=max(data['% Delta YTD'])+1.5*y_diff_scale, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-01-21', y=max(data['% Delta YTD'])+2*y_diff_scale, text='01/21 - 1st US COVID-19 Case')

    if latest_day >= datetime.strptime('2020-02-19', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-02-19', y0=min(data['% Delta YTD']), x1='2020-02-19', y1=max(data['% Delta YTD'])+1.5*y_diff_scale, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-02-19', y=max(data['% Delta YTD'])+2*y_diff_scale, text='02/19 - Market Record High')

    if latest_day >= datetime.strptime('2020-02-28', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-02-28', y0=min(data['% Delta YTD']), x1='2020-02-28', y1=max(data['% Delta YTD'])-.5*y_diff_scale, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-02-28', y=max(data['% Delta YTD'])+y_diff_scale, text='02/28 - 1st US COVID-19 Death')
        fig.add_annotation(x='2020-02-28', y=max(data['% Delta YTD']), text='02/28 - Market Correction (-10%)')

    if latest_day >= datetime.strptime('2020-03-09', '%Y-%m-%d'):
        fig.add_shape(dict(type="line", x0='2020-03-09', y0=min(data['% Delta YTD']), x1='2020-03-09', y1=max(data['% Delta YTD'])-1.5*y_diff_scale, 
                        line=dict(color='Black', width=0.1, dash="dot")))
        fig.add_annotation(x='2020-03-09', y=max(data['% Delta YTD'])-y_diff_scale, text='03/09 - Bear Market (-20%)')

    fig.update_annotations(dict(xref="x", yref="y", showarrow=True, arrowhead=7, ax=60, ay=0))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=True, zerolinewidth=0.05, zerolinecolor='Gray')
    return fig

### LAYOUT
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
        ', US market EOD closing prices only.']
    ),
    html.Br(),
    html.H5('Date'),
    html.Div(
        className = 'row',
        children = [
            html.Div(
                className = 'two columns',
                children = [
                    html.Strong(id = 'date-print'),
                    html.P(id='ytd-print')
                ]
            ),
            html.Div(
                className = 'ten columns',
                children = [
                    dcc.Slider(
                        id = 'date-slider',
                        min = 0,
                        max = DELTA_DAYS,
                        marks = {i:(EARLIEST_DATE + timedelta(days=i)).strftime('%Y/%m/%d') \
                            for i in range(int(DELTA_DAYS/8), (DELTA_DAYS+1-int(DELTA_DAYS/8)), int(DELTA_DAYS/4))},
                        value = DELTA_DAYS
                    ),
                ]
            )
        ]
    ),
    html.Hr(),
    html.H5('Key Indices'),
    html.Div(industry_overall_view(INDICES)),
    html.Br(),
    html.Hr(),
    html.H5('FAANG + Microsoft'),
    html.Div(industry_overall_view(FAANGM)),
    html.Br(),
    html.Hr(),
    html.H5('Airlines'),
    html.Div(industry_overall_view(AIRLINES)),
    html.Br(),
    html.Hr(),
    html.H5('Custom Stock vs Market Average'),
    html.Br(),
    html.Div(
        className = 'row',
        children = [
            html.Div(
                className = 'six columns',
                children = [
                    html.Br(),
                    html.P(html.B(id = 'custom-vs-market-result')),
                    html.P('Type stock ticker + press enter'),
                    dcc.Input(
                        id = 'custom-stock-input',
                        type = 'text',
                        debounce=True,
                        value = 'ZM'
                    ),
                    #html.P('Compare the custom stock\'s performance (% Delta YTD) to market average via. key indices.'),
                ]
            ),
            html.Div(
                className = 'six columns',
                children = [
                    html.Div(
                        className = 'row',
                        children = [
                            html.Div(
                                className = 'four columns',
                                children = [
                                    html.H2(html.B(id = 'custom-stock-price')),
                                    html.B(id = 'custom-stock-info-2'),
                                    dcc.Loading(html.P(id = 'custom-stock-ytd', style = {'height':'20px'}), color = '#222222', type = 'circle'),
                                ]
                            ),
                            html.Div(
                                className = 'four columns',
                                children = dcc.Loading(dcc.Graph(id = 'custom-stock-graph', style = gh), color = '#222222', type = 'circle'),
                            ),
                            html.Div(
                                className = 'four columns',
                                children = [
                                    html.Div(html.B(id = '^IXIC-info-custom')),
                                    dcc.Loading(html.P(id = '^IXIC-ytd-custom', style = {'height':'20px'}), color = '#222222', type = 'circle'),
                                    html.Div(html.B(id = '^GSPC-info-custom')),
                                    dcc.Loading(html.P(id = '^GSPC-ytd-custom', style = {'height':'20px'}), color = '#222222', type = 'circle'),
                                    html.Div(html.B(id = '^DJI-info-custom')),
                                    dcc.Loading(html.P(id = '^DJI-ytd-custom', style = {'height':'20px'}), color = '#222222', type = 'circle'),
                                ]
                            )
                        ]
                    ), 
                ]
            ),
        ]
    ),
    html.Br(),
    html.Br(),
    dcc.Loading(dcc.Graph('custom-vs-market-graph', style = gh), color = '#222222', type = 'circle'),
    #html.Div(output)
]

### MAIN LAYOUT
layout = html.Div(
    className = 'container',
    children = child
)