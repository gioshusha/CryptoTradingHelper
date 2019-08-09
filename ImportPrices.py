from binance.client import Client
import csv
import os
import pandas as pd
import constants
import statistics

client = Client(os.getenv("secret1"), os.getenv("secret2"))
def df(cr):
    klines = client.get_historical_klines(cr, Client.KLINE_INTERVAL_1HOUR, constants.Timeframe)
    x = 0
    TimeH = []
    PriceH = []
    AverageH = []
    STDEVHmin = []
    STDEVHmax = []
    volumeBuy = []
    volumeSell = []
    Diff=[]


    while x < constants.NUMBER:
        TimeH.append(pd.to_datetime(round(float(klines[len(klines) - x - 1][0])/1000/60/60,0), unit='h'))

        PriceH.append(float(klines[len(klines) - x - 1][4]))
        volumeBuy.append(float(klines[len(klines) - x - 1][9]))
        volumeSell.append(float(klines[len(klines) - x - 1][5])-float(klines[len(klines) - x - 1][9]))
        AverageH_1 = 0
        STDEVH_1 = []
        y = 0
        while y < 24:
            AverageH_1 = AverageH_1 + float(float(klines[len(klines) - x - 1 - y][4]))
            STDEVH_1.append(float(float(klines[len(klines) - x - 1 - y][4])))
            y = y + 1
        AverageH.append(round(AverageH_1/24,5))
        STDEVHmin.append(round(AverageH_1/24,5) - (statistics.stdev(STDEVH_1)*2))
        STDEVHmax.append(round(AverageH_1/24,5) + (statistics.stdev(STDEVH_1)*2))
        Diff.append(volumeBuy[x] - volumeSell[x])
        x = x + 1


    Data = {"Date":TimeH,
            "Price":PriceH,
            "Average":AverageH,
            "Bollmin":STDEVHmin,
            "Bollmax":STDEVHmax,
            "Buy":volumeBuy,
            "Sell":volumeSell,
            "Diff":Diff}
    df = pd.DataFrame(Data)

    return df
#print(df("ETHUSDT"))