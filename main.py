#main.py
import ccxt.pro
import asyncio
import logging
import time
import json
import pprint
import numpy as np
import sys
import datetime

from storagev2 import meta, table_ohlcv, table_orderbook, table_trades, table_ticker, table_logs
from sqlalchemy import create_engine

#symbols
btc_inverse_perp = 'BTC/USD:BTC'
btc_linear_perp = 'BTC/USDT:USDT'

#settings
timeframe = '1m'
orderbook_depth = 50
timeout = 10 #seconds
candle_limit = 1

print('Python version: ', sys.version_info)
if sys.version_info < (3,7):
    print("This script requires Python 3.7 or higher.")
    sys.exit(1)
print('CCXT version', ccxt.pro.__version__)
print('Supported exchanges:', ccxt.pro.exchanges)

engine = create_engine('sqlite:///data.db', echo = False)
meta.create_all(engine)

#https://github.com/ccxt/ccxt/blob/master/examples/ccxt.pro/py/one-exchange-different-streams.py
async def watch_order_book(exchange, symbol, orderbook_depth):
    '''
    Watch the order book for a specific symbol.
    Orderbook is unique from api, updates on deltas
    
    :param exchange: The exchange object
    :param symbol: The trading symbol
    :param orderbook_depth: The depth of the order book
    '''
    last_orderbook = None
    name = getattr(exchange, 'name')
    
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol, orderbook_depth)
                
            with engine.connect() as conn:
                command = table_orderbook.insert().values(
                    exchange = name,
                    symbol = orderbook['symbol'],
                    asks = orderbook['asks'],
                    bids = orderbook['bids'],
                    nonce = orderbook['nonce'],
                    created_at = orderbook['timestamp']
                    )
                conn.execute(command)
                conn.commit()
        
        except Exception as e:
            print(str(e))
            raise e
    
async def watch_trades(exchange, symbol):
    '''
    Watch the trades for a specific symbol.
    Trades are unique from the api
    
    :param exchange: The exchange object
    :param symbol: The trading symbol
    '''
    table_created = None
    name = getattr(exchange, 'name')
    
    while True:
        try:
            trades = await exchange.watch_trades(symbol)
            
            with engine.connect() as conn:
                for trade in trades:
                    command = table_trades.insert().values(
                    exchange = name,
                    trade_id = trade['id'],
                    order_id = trade['order'],
                    order_type = trade['type'],
                    trade_side = trade['side'],
                    takerormaker = trade['takerOrMaker'],
                    executed_price = trade['price'],
                    base_amount = trade['amount'],
                    cost = trade['cost'],
                    fee = trade['fee'],
                    fees = trade['fees'],
                    datetime = datetime.datetime.fromisoformat(trade['datetime']),
                    created_at = trade['timestamp']
                    )
                    
                    conn.execute(command)
                    conn.commit()
                    
        except Exception as e:
            print(str(e))
            raise e

async def watch_ohlcv(exchange, symbol, timeframe, candle_limit):
    #https://github.com/ccxt/ccxt/blob/master/examples/ccxt.pro/py/build-ohlcv-many-symbols.py
    '''
    Watch the OHLCV data for a specific symbol.

    :param exchange: The exchange object
    :param symbol: The trading symbol
    :param timeframe: The timeframe for the OHLCV data
    :param candle_limit: The number of candles to fetch
    '''
    last_candle = None
    name = getattr(exchange, 'name')
    
    while True:
        try:
            candle = await exchange.watch_ohlcv(symbol, timeframe, None, candle_limit)
            
            if last_candle is None:
                last_candle = candle
            
            #if timestamps are not equal
            if last_candle[0][0] != candle[0][0]:
                
                with engine.connect() as conn:
                    command = table_ohlcv.insert().values(
                        exchange = name,
                        symbol = symbol,
                        open_price = last_candle[0][1],
                        high_price = last_candle[0][2],
                        low_price = last_candle[0][3],
                        close_price = last_candle[0][4],
                        candle_volume = last_candle[0][5],
                        utc_timestamp = last_candle[0][0]
                        )
                
                    conn.execute(command)
                    conn.commit()
            last_candle = candle
            
        except Exception as e:
            print(str(e))
            raise e
            
async def watch_ticker(exchange, symbol):
    '''
    Watch the ticker of an exchange for a specific symbol.

    :param exchange: The exchange object
    :param symbol: The trading symbol
    '''
    name = getattr(exchange, 'name')
    last_ticker = None
        
    while True:
        try:
            ticker = await exchange.watch_ticker(symbol)
            
            command = table_ticker.insert().values(
                exchange = name,
                symbol = symbol,
                ask = ticker['ask'],
                askvolume = ticker['askVolume'],
                bid = ticker['bid'],
                bidvolume = ticker['bidVolume'],
                open_24h = ticker['open'],
                high_24h = ticker['high'],
                low_24h = ticker['low'],
                close_24h = ticker['close'],
                last_price = ticker['last'],
                vwap = ticker['vwap'],
                previousclose_price = ticker['previousClose'],
                price_change = ticker['change'],
                percentage_change = ticker['percentage'],
                average_price = ticker['average'],
                basevolume = ticker['baseVolume'],
                quotevolume = ticker['quoteVolume'],
                info = ticker['info'],
                datetime = datetime.datetime.fromisoformat(ticker['datetime']),
                created_at = ticker['timestamp']
                )
            
            #create timeless dict to check for uniqueness
            unique_ticker = ticker.copy()
            removal = ['timestamp', 'info', 'datetime']
            for key in removal:
                unique_ticker.pop(key)

            if last_ticker is None:
                last_ticker = [ticker, unique_ticker]                
                with engine.connect() as conn:
                    conn.execute(command)
                    conn.commit()
                    
            if unique_ticker != last_ticker[1]:
                
                #if they are not equal insert new ticker
                with engine.connect() as conn:
                    conn.execute(command)
                    conn.commit()
                    
                                
                #set last ticker to new one
                last_ticker[0] = ticker
                last_ticker[1] = unique_ticker
            
        except Exception as e:
            print(str(e))
            raise e

async def main():    
    exchange = ccxt.pro.bybit({'newUpdates':True,'enableRateLimit': True, 'verbose':False})
    
    await exchange.load_markets()        
    symbol = btc_inverse_perp
    
    loops = []
    if exchange.has["watchOHLCV"]:
        loops.append(
            watch_ohlcv(exchange, symbol, timeframe, candle_limit))
    if exchange.has["watchTicker"]:
        loops.append(
            watch_ticker(exchange, symbol))
    if exchange.has["watchTrades"]:
        loops.append(
            watch_trades(exchange, symbol))
    if exchange.has["watchOrderBook"]:
        loops.append(
            watch_order_book(exchange, symbol, orderbook_depth))
    
    while True:
        await asyncio.gather(*loops)
    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())
