from binance.client import Client
import pandas as pd
import os

client = Client(os.getenv("secret1"), os.getenv("secret2"))
def getServerTime():
    time_res = client.get_server_time()
    return pd.to_datetime(round(time_res['serverTime']/1000/60,0), unit='m')

#print(pd.to_datetime(getServerTime(), unit='ms'))
#print(pd.to_datetime(round(getServerTime()/1000/60/60,0), unit='h'))