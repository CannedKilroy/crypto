#main.py
import ccxt.pro
import asyncio
import logging
import time
import json
import pprint
import numpy as np
import sys

from settings import (
btc_inverse_perp,
btc_linear_perp,
timeframe,
orderbook_depth,
timeout,
candle_limit,
tables
)
from storage import Database, ConnectionManager

print('Python version: ', sys.version_info)
print('CCXT version', ccxt.pro.__version__)
print('Supported exchanges:', ccxt.pro.exchanges)

#https://github.com/ccxt/ccxt/blob/master/examples/ccxt.pro/py/one-exchange-different-streams.py
async def watch_order_book(exchange, symbol, orderbook_depth, db):
    '''
    Watch the order book for a specific symbol.

    :param exchange: The exchange object
    :param symbol: The trading symbol
    :param orderbook_depth: The depth of the order book
    :param db: The database object
    '''
    while True:
        try:
            
            orderbook = await exchange.watch_order_book(symbol, orderbook_depth)
            db.insert_one(table_name = 'orderbook',
                          data = (orderbook['symbol'],
                                       orderbook['timestamp'],
                                       json.dumps(orderbook['asks']),
                                       json.dumps(orderbook['bids']),
                                       orderbook['nonce'],
                                       orderbook['datetime'])
                          )
        except Exception as e:
            print(str(e))
            raise e
    
async def watch_trades(exchange, symbol, db):
    '''
    Watch the trades for a specific symbol.

    :param exchange: The exchange object
    :param symbol: The trading symbol
    :param db: The database object
    '''
    while True:
        try:
            
            trades = await exchange.watch_trades(symbol)
            for trade in trades:
                
                #convert from scinetific notation to decimal
                cost = np.format_float_positional(trade['cost'])
                
                db.insert_one(table_name = 'trades',
                          data = (trade['symbol'],
                                  trade['timestamp'],
                                  trade['id'],
                                  trade['order'],
                                  trade['type'],
                                  trade['side'],
                                  trade['takerOrMaker'],
                                  trade['price'],
                                  trade['amount'],
                                  cost, #decimal, in base currency
                                  json.dumps(trade['info']),
                                  trade['datetime']
                                  ))
        
        except Exception as e:
            print(str(e))
            raise e        


async def watch_ohlcv(exchange, symbol, timeframe, candle_limit, db):
    #https://github.com/ccxt/ccxt/blob/master/examples/ccxt.pro/py/build-ohlcv-many-symbols.py
    '''
    Watch the OHLCV data for a specific symbol.

    :param exchange: The exchange object
    :param symbol: The trading symbol
    :param timeframe: The timeframe for the OHLCV data
    :param candle_limit: The number of candles to fetch
    :param db: The database object
    '''
    last_candle = None
    
    while True:
        try:
            candle = await exchange.watch_ohlcv(symbol, timeframe, None, candle_limit)
            print(candle)
            if last_candle is None:
                last_candle = candle
            
            if last_candle[0][0] != candle[0][0]:
                db.insert_one(table_name='ohlcv',
                              data=(symbol,) + tuple(last_candle[0]))
            
            last_candle = candle
            db.return_all('ohlcv')
            
        except Exception as e:
            print(str(e))
            raise e

async def watch_ticker(exchange, symbol, db):
    '''
    Watch the ticker of an exchange for a specific symbol.

    :param exchange: The exchange object
    :param symbol: The trading symbol
    :param db: The database object
    
    '''
    while True:
        try:
            ticker = await exchange.watch_ticker(symbol)
            db.insert_one(table_name = 'ticker',
                          data = (ticker['symbol'],
                                  ticker['timestamp'],
                                  ticker['ask'],
                                  ticker['askVolume'],
                                  ticker['bid'],
                                  ticker['bidVolume'],
                                  ticker['open'],
                                  ticker['high'],
                                  ticker['low'],
                                  ticker['close'],
                                  ticker['vwap'],
                                  ticker['previousClose'],
                                  ticker['change'],
                                  ticker['percentage'],
                                  ticker['average'],
                                  ticker['baseVolume'],
                                  ticker['quoteVolume'],
                                  ticker['last'],
                                  json.dumps(ticker['info']),
                                  ticker['datetime']
                                  ))
        
        except Exception as e:
            print(str(e))
            raise e

async def main():
    
    #create db and tables
    db = Database('data')
    for name, columns in tables.items():
        db.create_table(table_name = name,
                        columns = columns, 
                        drop_table = True,
                        )
    
    
    exchange = ccxt.pro.bybit({'newUpdates':True,'enableRateLimit': True, 'verbose':False})
    await exchange.load_markets()
    symbol = btc_inverse_perp
    
    loops = []
    
    
    if exchange.has["watchOHLCV"]:
        loops.append(watch_ohlcv(exchange, symbol, timeframe, candle_limit, db))
    
    
    if exchange.has["watchTicker"]:
        loops.append(watch_ticker(exchange, symbol, db))
    
    
    if exchange.has["watchTrades"]:
        loops.append(watch_trades(exchange, symbol, db))
    
    
    if exchange.has["watchOrderBook"]:
        loops.append(watch_order_book(exchange, symbol, orderbook_depth, db))
    
    while True:
        try:
            loops
            await asyncio.gather(*loops)
        
        #https://docs.ccxt.com/#/?id=error-handling
        except ccxt.DDoSProtection as e:
            print(f"{exchange} ddos protected. Retrying in {timeout} seconds.")
            db.insert_one(table_name = 'logs',
                          data = (time.time(), e.args[0]))
            time.sleep(timeout)
            continue
        
        except ccxt.NetworkError as e:
            print(f"{exchange} failed due to a network error: {str(e)}")  
            db.insert_one(table_name = 'logs',
                          data = (time.time(), e.args[0]))            
            time.sleep(timeout)
            continue
        
        except ccxt.ExchangeError as e:
            print(f"{exchange} failed due to an exchange error: {str(e)}")
            db.insert_one(table_name = logs,
                          data = (time.time(), e.args[0]))
            time.sleep(timeout)
            continue
        
        except Exception as e:
            print(type(e).__name__, str(e))
            db.insert_one(table_name = 'logs',
                          data = (time.time(), e.args[0]))
            time.sleep(timeout)            
            continue
            
    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())
