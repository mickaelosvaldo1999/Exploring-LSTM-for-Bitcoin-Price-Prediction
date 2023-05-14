"""
    Comments section 
    type:
        safe: BTC/stablecoin or fiat currency pair
        risky: BTC/Altcoin pair
"""
import json
import pair
import time
import BTools

#List of objects
pairList = []
#Getting the list of pairs
req = BTools.getExchangeInfo()

#ordering the list
for i in req["symbols"]:
    if i["baseAsset"] == "BTC":
        if i["quoteAsset"] in BTools.stable:
            pairList.append(pair.pair(i["symbol"],"safe",i["quoteAsset"]))
        else:
            pairList.append(pair.pair(i["symbol"],"risky",i["quoteAsset"]))
    elif i["quoteAsset"] == "BTC":
        if i["baseAsset"] in BTools.stable:
            pairList.append(pair.pair(i["symbol"],"safe",i["baseAsset"]))
        else:
            pairList.append(pair.pair(i["symbol"],"risky",i["baseAsset"]))

# output 
with open("src/pairs.json", 'w') as f:
    f.truncate(0)
    #turn a list of objects into a serialized list of objects
    jsonized = json.dumps(pairList[:], indent=4, cls=pair.CEncoder)
    #including header
    file = [
        {"version": "1.0"},
        {"timestamp": (time.time_ns() + 500000) // 1000000},
        {"description": "This file contains a list of all the pairs listed on Binance, with their type (safe or risky) and their target (the stablecoin or fiat currency they are paired with)."},
        {"data": json.loads(jsonized)}
        ]
    
    json.dump(file, f, indent=4)
    
# Closing file
f.close()