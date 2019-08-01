import pandas as pd
from binance.client import Client
import os
import constants


def GetVolume(cr):
    client = Client(os.getenv("secret1"), os.getenv("secret2"))
    trades = client.get_klines(symbol=cr, interval=Client.KLINE_INTERVAL_1HOUR)

    tickers = client.get_ticker(symbol=cr)
    helper0  =[]
    helper1 = []
    helper2 = []
    helper3 = []

    for tr in trades:
        helper0.append(tr)
    x = 0
    while x < constants.NUMBER:
        helper1.append(round(float(helper0[len(helper0) - 1 - x][9]),2))
        helper2.append(round(float(helper0[len(helper0) - 1 - x][5]),2))
        helper3.append(round(float(helper0[len(helper0) - 1 - x][5]),2) - round(float(helper0[len(helper0) - 1 - x][9]),2))
        x = x + 1

    Data = {"Buy":helper1,
            "Sell":helper3,
            "Total":helper2,}
    df = pd.DataFrame(Data)
    return df