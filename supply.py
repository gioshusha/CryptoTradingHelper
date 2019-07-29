from binance.client import Client
import pandas as pd
import os
import time

client = Client(os.getenv("secret1"), os.getenv("secret2"))
def loadData(cr):
  depth = client.get_order_book(symbol=cr)
  x1 = []
  y1 = []
  xy1 = []
  x = 0
  while len(depth["bids"])>x:
    x1.append(float(depth["bids"][x][0]))
    y1.append(float(depth["bids"][x][1]))
    xy1.append(float(depth["bids"][x][0]) * float(depth["bids"][x][1]))
    x = x + 1
  x2 = []
  y2 = []
  xy2 = []
  x = 0
  while len(depth["asks"])>x:
    x2.append(float(depth["asks"][x][0]))
    y2.append(float(depth["asks"][x][1]))
    xy2.append(float(depth["asks"][x][0]) * float(depth["asks"][x][1]))
    x = x + 1

  x = 0
  sum1 = 0
  sum2 = 0

  sum3 = 0
  sum4 = 0

  while x < 100:
    sum1 = sum1 + xy1[x]
    sum2 = sum2 + y1[x]
    sum3 = sum3 + xy2[x]
    sum4 = sum4 + y2[x]
    x = x + 1
  maximumAsk = 0
  maximumbid = 0
  askpr = 0
  bidpr = 0
  x = 0
  while x < 100:
    if maximumAsk < y2[x]:
      maximumAsk = y2[x]
      askpr = x2[x]
    if maximumbid < y1[x]:
      maximumbid = y1[x]
      bidpr = x1[x]
    x = x + 1
  bids = sum1 / sum2
  asks = sum3 / sum4
  total = (bids + asks)/2
  df = []
  df.append(round(sum1,2))
  df.append(round(sum3,2))
  df.append(round(bids,2))
  df.append(round(asks,2))
  return df