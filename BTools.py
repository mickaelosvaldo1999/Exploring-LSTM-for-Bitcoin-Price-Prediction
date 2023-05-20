"""
     API tools for projects based on the Binance exchange.
     Author: Mickael de Oliveira
     Version: 1.0
"""
import requests

#Request controller to dismiss IP ban
def requestController(url):
    req = requests.get("https://api.binance.com/api/v3/" + url)
    #TODO Verifying the status code on return response
    if 0 !=0:
        print("too many requests, waiting 429s")
    else:
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

#Request data of a pair
#symbol,startime TIMESTAMP, interval "TIMESTAMP 15m 1h", candle limit and coin volume selector (0 base 1 quote)
def getCandlestick(start, pair, interval,limit,ctr):
    url = f"klines?symbol={pair}&interval={interval}&startTime={start}&limit={limit}"
    req = requestController(url)
    req = req.json()
    response = []
    for i in req:
        if ctr == 0:
            #returns open time, average price, volume, and trades
            response.append([i[0], (float(i[1]) + float(i[2]))/2, i[5], i[8]])
        else:
            #returns open time, average price, quote volume and trades
            response.append([i[0], (float(i[1]) + float(i[2]))/2, i[7], i[8]])
    return response

print(getCandlestick(1682910000000,"BTCUSDT", "15m",1000,1))