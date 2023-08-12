Cryptocurrency Futures Data Capture Tool

Python script that captures and stores realtime cryptocurrency websocket data asynchronously, using the ccxt library and sqlalchemy with sqlite. Any ccxt supported exchange and symbol should work. After exchange connection is made and tables created, websocket OHLCV, ticker, trades, and orderbook data are checked for uniquness and then inserted into a their own table.

Prerequisites:
Python 3.7 <=
SQLalchemy

Usage:
Clone repo to local machine
Run:
pip install -r requirements.txt
Run:
main.py

Note:
The inverse bitcoin futures contract on bybit generates approximatly 15-25 gigabytes of data a day.
Adding more exchanges / symbols to watch would generate alot of data 

TODO:
- function that translates bybit symbol to ccxt symbol
- add requirements.txt
- add exchange symbol and humanreadable symbol to tables
- async sqlalchemy, eventually time series database as dataset grows
- add config file for ohlcv timeframe, exchanges, symbols, db location, orderbook depth, timeout
- input for db
- wrap main to run continously and handle errors better
