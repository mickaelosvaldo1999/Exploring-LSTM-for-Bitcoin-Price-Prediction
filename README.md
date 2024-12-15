# Exploring LSTM for Bitcoin Price Prediction
This research focuses on analyzing the relationship
between Bitcoin prices, trading rates and volume to predict
prices in 15-minute candle intervals. The study proposes the
use of Long Short-Term Memory (LSTM) neural network for
developing a reliable prediction model. Historical Bitcoin data
was obtained from the Binance API and underwent collection
and preprocessing. The performance of the prediction model is
evaluated against the real one. The findings contribute to the
analysis of cryptocurrency markets, enabling investors to make
informed real-time decisions, facilitating the development of
advanced trading algorithms and risk management strategies in
the cryptocurrency space.

## Overview
An implementation of a LSTM on bitcoin chart.

## Dataset
Price, trading rates, and volume of Binance transactions for Bitcoin pairs in 2020, with a 15-minute interval.

### Dataset features list

#### Timestamp: (GMT -3):
Milliseconds time from 2017-31-12 to 2023-01-06.

#### volumeRisky:
Volume from Bitcoin to altcoins, memecoins or NFTs.

#### volumeSafe
Volume from Bitcoin to FIAT or Stable coins.

#### tradesRisky
Volume from Bitcoin to altcoins, memecoins or NFTs.

#### tradesSafe
Trades from Bitcoin to FIAT or Stable coins.

#### price
Price in USDT

### Why are these features helpful?
The crypto market operates on cycles driven by FOMO (Fear of Missing Out) and FUD (Fear, Uncertainty, and Doubt). Every four years, Bitcoin undergoes a halving, reducing the mined supply by half. This dataset focuses on the 2020 halving, providing insights into the flow of money during this period.

## General features
* Integrated binance API module
* Native Threads support on request
* Easy to use and large documentation
* Http remaker (personalized HTTP response)

## License
This code is distributed under the GPL-3.0 license. See the LICENSE file for more information.
