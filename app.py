import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import constants
import rss
import plotly.graph_objects as go
import supply
import ImportPrices

#end imports
#style modification:
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
# styles provided by dash.plot.ly
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#import prices from external library
rssdata = rss.News()


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
    html.H1(children='Platform'),
    #dropdown Manu for selecting cryptocurrency
    dcc.Dropdown(
        id='CryptoChose',
        options=[
            {'label': 'ETH', 'value': 'ETHUSDT'},
            {'label': 'BTC', 'value': 'BTCUSDT'},
            {'label': 'XRP', 'value': 'XRPUSDT'},
            {'label': 'PAX', 'value': 'PAXUSDT'}
        ],
        style={'height': '15px','width': '150px','margin-bottom':'18px'},
        value='ETHUSDT',
        clearable=False
    ),
    #live update graph line graph
    html.Div([
        dcc.Graph(id='update_graph_live'),
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

#live updates for supply
@app.callback(Output('update_graph_live', 'figure'),
              [Input('interval-component', 'n_intervals')],
              [dash.dependencies.State('CryptoChose', 'value')])
def update_graph_live(n,value):
    df = ImportPrices.df(value)
    fig = {
        'data': [
            {'x': df["Date"], 'y': df["Price"], 'type': 'line','mode':'lines+markers', 'name': "Price"},
            {'x': df["Date"], 'y': df["Average"], 'type': 'line', 'name': "24H Average"},
            {'x': df["Date"], 'y': df["Bollmin"], 'type': 'line', 'name': "BOLL low"},
            {'x': df["Date"], 'y': df["Bollmax"], 'type': 'line', 'name': "BOLL high"}
        ],
        'layout': {
            'title': value,
            'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                    }
        }
    }
    return fig

@app.callback(Output('update_graph_live2', 'figure'),
              [Input('interval-component2', 'n_intervals')],
              [dash.dependencies.State('CryptoChose', 'value')])
def update_graph_live2(n,value):
    supplydata = supply.loadData(value)
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
    max_rows = 5
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#start app
if __name__ == '__main__':
    app.run_server(debug=True)