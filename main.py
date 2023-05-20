import json
import csv
import BTools as bt
import pandas as pd
file = json.load(open("src/pairs.json"))

now = []

#getting bitcoin prices
response = bt.getCandlestick(1682910000000,"BTCUSDT", "15m",1200,1)
for i in response:
    now.append({"time": i[0],"volumeRisky": 0,"volumeSafe": 0,"tradeRisky": 0,"tradeSafe": 0,"price": i[2],"flag": 0})
    data = pd.DataFrame(data=now, columns=["time","volumeRisky","volumeSafe","tradeRisky","tradeSafe","price","flag"], index=None)

print(data)