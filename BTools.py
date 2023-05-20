"""
     API tools for projects based on the Binance exchange.
     Author: Mickael de Oliveira
     Version: 1.0
"""
import requests
from BTime import *

def requestController(url):
    """Controller for requests to Binance API to dismiss ip ban"""
    req = requests.get("https://api.binance.com/api/v3/" + url)
    #Verifying the status code on return response
    if req.status_code == 429:
        print("too many requests, waiting for binance to unban us")
        pause()
    return req

#List of stablecoins or fiat currencies listed on Binance
stable = [
    'USDT', 'BUSD', 'USDC', 'TUSD', 'DAI', 'IDRT', 'UAH', 'RUB', 'EUR', 'NGN', 'GBP', 'TRY', 'ZAR', 'AUD', 'BRL', 'MXN', 'CAD', 'JPY', 'INR', 'KRW', 'CNY', 'RUB', 'TRY', 'UAH'
    ]

#Request a complete exchange info from Binance
def getExchangeInfo():
    url = "exchangeInfo"
    req = requestController(url)
    return req.json()

def getCandlestick(start, pair, interval,limit,ctr):
    """
    Request data of a pair
    symbol,startime TIMESTAMP, interval "15m, 1h", candle limit, volume selector (0 base 1 quote)
    """
    response = []
    #dividing the request in 1000 candlesticks
    while limit > 1000:
        limit -= 1000
        url = f"klines?symbol={pair}&interval={interval}&startTime={start}&limit=1000"
        req = requestController(url)
        req = req.json()
        for i in req:
            if ctr == 0:
                #returns open time, close time, average price, volume, and trades
                response.append([i[0], i[6], (float(i[1]) + float(i[2]))/2, i[5], i[8]])
            else:
                #returns open time, close time, average price, quote volume and trades
                response.append([i[0], i[6], (float(i[1]) + float(i[2]))/2, i[7], i[8]])
        
        #updating the start time
        if (limit*getTime(interval)) > (now() - response[-1][0]):
            print(limit*getTime(interval))
            print(now() - response[-1][0])
            raise Exception("The last candlestick is in the future") 
        else:
            start = response[-1][1]
        
        
    #making the last request
    url = f"klines?symbol={pair}&interval={interval}&startTime={start}&limit={limit}"
    req = requestController(url)
    req = req.json()
    for i in req:
        if ctr == 0:
            #returns open time, close time, average price, volume, and trades
            response.append([i[0], i[6], (float(i[1]) + float(i[2]))/2, i[5], i[8]])
        else:
            #returns open time, close time, average price, quote volume and trades
            response.append([i[0], i[6], (float(i[1]) + float(i[2]))/2, i[7], i[8]])
    return response