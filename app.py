#dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import plotly.tools as tls
from plotly.subplots import make_subplots
#external imports
import pandas as pd
#internal imports (I am tring to seperate code as much as possible)
import constants
import rss
import supply
import ImportPrices
import Time
#end imports
#style modification:
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
# styles provided by dash.plot.ly
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


#generate table with information on cryptocurrency
def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#main body of dash.py
app.layout = html.Div(children=[
    #title
    html.H1(children='ProjectCH'),
    #Server Time
    html.Div([
        html.H4(id='ServerTime'),
        dcc.Interval(
            id='SVTIME',
            interval=constants.fastIntervals*60, # in milliseconds
            n_intervals=1
    )]),
    #dropdown Manu for selecting cryptocurrency
    dcc.Dropdown(
        id='CryptoChose',
        options=[
            {'label': 'ETH', 'value': 'ETHUSDT'},
            {'label': 'BTC', 'value': 'BTCUSDT'},
            {'label': 'BNB', 'value': 'BNBUSDT'},
            {'label': 'XPR', 'value': 'XRPUSDT'}
        ],
        style={'height': '15px','width': '150px','margin-bottom':'18px'},
        value='ETHUSDT',
        clearable=False
    ),
    #MAIN GRAPH live update graph line graph
    html.Div([
        dcc.Graph(id='update_graph_live',style={'height':600}),
        dcc.Interval(
            id='interval-component2',
            interval=constants.fastIntervals, # in milliseconds
            n_intervals=1
        )]),
    #current price monitoring
    html.Div([
        html.H4(id='PriceLive'),
        dcc.Interval(
            id='interval-component3',
            interval=constants.fastIntervals, # in milliseconds
            n_intervals=1
    )]),
    #information about supply and demand
    html.Div([
        html.H4(id='SupplyUpdate'),
        dcc.Interval(
            id='interval-component4',
            interval=constants.fastIntervals, # in milliseconds
            n_intervals=1
    )],className="six columns"),
    #pie chart regarding supply and demand
    html.Div([
        dcc.Graph(id='update_graph_live2'),
        dcc.Interval(
            id='interval-component',
            interval=constants.fastIntervals, # in milliseconds
            n_intervals=1
        )],className="six columns"),
    #placeHolder I will work on this afterwards
    html.Div([
            html.H1(children='PlaceHolder for Analysis'),
        ],className="six columns"),
    # html table
    #generate_table(rssdata)
    html.Div([
        html.P(id='RSSupdate'),
        dcc.Interval(
            id='interval-component5',
            interval=constants.RSSUpdates, # in milliseconds
            n_intervals=1
    )])
    #end of main div
    ],style={'textAlign': 'center',
        'color': colors['text'],
        'background':colors['background']
        })

#MAIN GRAPH UPDATE: live updates for Line Grahp.
@app.callback(Output('update_graph_live', 'figure'),
              [Input('interval-component', 'n_intervals')],
              [dash.dependencies.State('CryptoChose', 'value')])
def update_graph_live(n,value):
    df = ImportPrices.df(value)
    print("Trying to Update")
    #create table
    fig = make_subplots(rows=2, cols=1)
    #price update
    fig.append_trace(go.Scatter(
        name='Price',
        x=df["Date"],
        y=df["Price"],
        mode='lines+markers',
    ), row=1, col=1)
    fig.append_trace(go.Scatter(
        name='Average',
        x=df["Date"],
        y=df["Average"],
    ), row=1, col=1)
    fig.append_trace(go.Scatter(
        name='Bollmin',
        x=df["Date"],
        y=df["Bollmin"],
    ), row=1, col=1)
    fig.append_trace(go.Scatter(
        name='Bollmax',
        x=df["Date"],
        y=df["Bollmax"],
    ), row=1, col=1)
    fig.append_trace(go.Bar(
        name='Volume Buy',
        x=df["Date"],
        y=df["Buy"],
        marker_color='rgb(0, 255, 0)'
    ), row=2, col=1)
    fig.append_trace(go.Bar(
        name='Volume Buy',
        x=df["Date"],
        y=df["Sell"],
        marker_color='rgb(255, 0, 0)'
    ), row=2, col=1)
    fig.update_layout(
        {
            'title': value,
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
                },
            'barmode':'stack'
        },
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    return fig


#Order Book Update
@app.callback(Output('update_graph_live2', 'figure'),
              [Input('interval-component2', 'n_intervals')],
              [State('CryptoChose', 'value')])
def update_graph_live2(n,crypto):
    supplydata = supply.loadData(crypto)
    lbls = ['Want To Buy','Want To Sell']
    vlus = [supplydata[0],supplydata[1]]
    clrs = ['rgb(0, 255, 0)','rgb(255, 0, 0)']
    fig = {
        'data': [
            go.Pie(labels=lbls, values=vlus,marker_colors=clrs)
        ],
        'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                    }
        }
    }
    return fig
# functions start here mostly live update functions.:
#live price update
@app.callback(Output('PriceLive', 'children'),
              [Input('interval-component3', 'n_intervals')],
              [dash.dependencies.State('CryptoChose', 'value')])
def PriceLive(n,value):
    PriceData = ImportPrices.df(value)
    return "Price: " + str(PriceData["Price"][0]) + " Change last 24H: " + str(round(PriceData["Price"][0]/PriceData["Price"][23]*100,2)) + "%"


#get Live Supply and demand prices
@app.callback(Output('SupplyUpdate', 'children'),
              [Input('interval-component4', 'n_intervals')],
              [dash.dependencies.State('CryptoChose', 'value')])
def PriceLive(n,value):
    supplydata = supply.loadData(value)
    return " Want To Buy: " + str(round(supplydata[2],4)) + " Want To Sell: " + str(round(supplydata[3],4))

#RSS table update
@app.callback(Output('RSSupdate', 'children'),
              [Input('interval-component5', 'n_intervals')])
def RSSupdate(n):
    dataframe = rss.News()
    max_rows = 10
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


#Live Update Of Time
@app.callback(Output('ServerTime', 'children'),
              [Input('SVTIME', 'n_intervals')])
def ServerTime(n):
    time = Time.getServerTime()
    return time

#get Live Supply and demand prices
#start app
if __name__ == '__main__':
    app.run_server(debug=True)