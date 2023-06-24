"""
     API tools for projects based on the Binance exchange.
     Author: Mickael de Oliveira
     Version: 1.0
"""
from typing import Any
from BTime import *
import requests
from BThreads import bThread

class requester():
    """
        ### Custom request class to handle erros and control spam rate
        
        #### Usage: get(route) for a get request
        
        #### multiGet(routeList) for requests running in parallel
        
        #### Be careful when using multhreading, this class is not thread safe
    """
    def get(self,route: str):
        controller = True
        while controller:
            """Send a get request for a determined route"""
            try:
                req = requests.get("https://api.binance.com/api/v3/" + route)
                #Verifying the status code on return response
                if req.status_code == 429:
                    print("too many requests, waiting for binance to unban us")
                    pause()
                elif req.status_code == 200:
                    controller = False
                else:
                    print("Error when requesting: ", req.status_code)
            except Exception as exc:
                print("Error when requesting: ", exc)
        return req
    
    def multiGet(self,routeList: list):
        """Send a list of get requests in parallel"""
        responses = []
        for i in routeList:
            #Creating a thread for each request
            responses.append(bThread(target = self.get, args = (i,)).start())
        
        for i in responses:
            #Waiting for all threads to finish
            i.join()
            
        return responses

#List of stable coins or fiat currencies listed on Binance
STABLE = [
    'USDT', 'BUSD', 'USDC', 'TUSD', 'DAI', 'IDRT', 'UAH', 'RUB', 'EUR', 'NGN', 'GBP', 'TRY', 'ZAR', 'AUD', 'BRL', 'MXN', 'CAD', 'JPY', 'INR', 'KRW', 'CNY', 'RUB', 'TRY', 'UAH'
    ]

#Request a complete exchange info from Binance
def getExchangeInfo():
    url = "exchangeInfo"
    req = requester()
    req = req.get(url)
    return req.json()

def getCandlestick(start, pair, interval,limit,ctr):
    """
    ### Request data of a pair
    #### startime TIMESTAMP, pair, interval "15m, 1h", candle limit, volume selector (0 base 1 quote)
    
    #### returns open time, close time, close price, base/quote volume, and trades
    """
    response = []
    #dividing the request in 1000 candlesticks
    while limit > 1000:
        limit -= 1000
        url = f"klines?symbol={pair}&interval={interval}&startTime={start}&limit=1000"
        req = requester()
        req = req.get(url)
        req = req.json()
        for i in req:
            if ctr == 0:
                #returns open time, close time, close price, base volume, and trades
                response.append([int(i[0]), int(i[6]), float(i[4]), float(i[5]), int(i[8])])
            else:
                #returns open time, close time, close, quote volume and trades
                response.append([int(i[0]), int(i[6]), float(i[4]), float(i[7]), int(i[8])])
        
        #updating the start time
        if (limit*getTime(interval)) > (now() - response[-1][0]):
            print(limit*getTime(interval))
            print(now() - response[-1][0])
            raise Exception("The last candlestick is in the future") 
        else:
            start = response[-1][1]
        
        
    #making the last request
    url = f"klines?symbol={pair}&interval={interval}&startTime={start}&limit={limit}"
    req = requester()
    req = req.get(url)
    req = req.json()
    for i in req:
        if ctr == 0:
            #returns open time, close time, close price, base volume, and trades
            response.append([int(i[0]), int(i[6]), float(i[4]), float(i[5]), int(i[8])])
        else:
            #returns open time, close time, close, quote volume and trades
            response.append([int(i[0]), int(i[6]), float(i[4]), float(i[7]), int(i[8])])
    return response

class pair():
    """ Pair class to handle pairs of coins"""
    def __init__(self,base: str,quote: str):
        self.base = base
        self.quote = quote
    
    def __str__(self):
        return self.base + self.quote

    def isSafe(self):
        if self.base in STABLE or self.quote in STABLE:
            return True
        else:
            return False
    
    def existsOnTime(self,time):
        """Return true if the pair exists on the given time"""
        temp = getCandlestick(time, self, "1m", 1, 0)
        if temp == []:
            return False
        else:
            if temp[0][0] < time + 60000:
                return True
            else:
                return False
    
    def getBase(self):
        """Return the base coin"""
        return self.base
    
    def getQuote(self):
        """Return the quote coin"""
        return self.quote
    
    

class pairs():
    def get(self,coin: str, timeStart = 0, timeEnd = -1):
        """
        ### Get all pairs with a given coin
        
        #### coin: str, coin to be searched
        
        #### timeStart: int, timestamp in milliseconds to check if the pair exists on the given time (now = 0)
        
        #### timeEnd: int, timestamp in milliseconds to check if the pair exists on the given time (no check = -1)
        """
        req = getExchangeInfo()
        self.pList = []
        for i in req['symbols']:
            if i['baseAsset'] == coin:
                self.pList.append(pair(i['baseAsset'],i['quoteAsset']))
            elif i['quoteAsset'] == coin:
                self.pList.append(pair(i['baseAsset'],i['quoteAsset']))
        
        #verify if the pair exists in determined time
        if timeStart == 0:
            timeStart = now() - 600000
        
        #verify if the pair exists on starting time
        self.checkList(timeStart)
        
        #Handling timeEnd
        if timeEnd != -1:
            if timeEnd < timeStart and timeEnd != 0:
                raise Exception("timeEnd must be greater than timeStart")
            
            elif timeEnd > now() - 600000:
                raise Exception("timeEnd must be less than now")
            
            elif timeEnd == 0:
                timeEnd = now() - 600000
                self.checkList(timeEnd)   
            
            else:
                self.checkList(timeEnd)
                                                      
                    
        return self.pList
    
    def checkList(self,time: int):
        threadList = []
        responses = []
        for i in self.pList:
            #Creating a thread for each request
            threadList.append(bThread(target = i.existsOnTime, args=(time,)))
        
        for i in threadList:
            #Starting all threads
            i.start()
            
        for i in threadList:
            #Waiting for all threads to finish and saving the response
            responses.append(i.join())
        
        j = 0
        for i in responses:
            if i == False:
                del self.pList[j]
                j -= 1
            j += 1 