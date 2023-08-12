#datastorage
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, JSON, REAL, DATETIME, INT, UniqueConstraint
meta = MetaData()

table_orderbook = Table(
   'orderbook', 
   meta, 
   Column('id', Integer, primary_key = True),
   Column('exchange', String, index = True, nullable = False),
   Column('symbol', String, index = True, nullable = False),
   Column('asks', JSON, nullable = False),
   Column('bids', JSON, nullable = False),
   Column('nonce', String, nullable = True),
   Column('created_at', INT, nullable = False, index = True)
   )

table_ticker = Table(
    'ticker',
    meta,
    Column('id', Integer, primary_key = True),
    Column('exchange', String, index = True),
    Column('symbol', String, index = True),
    Column('ask', REAL),
    Column('askvolume', REAL),
    Column('bid', REAL),
    Column('bidvolume', REAL),
    Column('open_24h', REAL), #OHLCV
    Column('high_24h', REAL),
    Column('low_24h', REAL),
    Column('close_24h', REAL),
    Column('last_price',REAL), #same as close
    Column('vwap', REAL),
    Column('previousclose_price', REAL),
    Column('price_change', REAL), #last-open
    Column('percentage_change', REAL),
    Column('average_price', REAL),
    Column('basevolume', REAL),
    Column('quotevolume', REAL),
    Column('info', JSON), #original ticker data from exchange
    Column('datetime', DATETIME),
    Column('created_at', INT, index = True)
)

table_trades = Table(
    'trades',
    meta,
    Column('id', Integer, primary_key = True),
    Column('exchange', String, index = True),
    Column('symbol', String, index = True),
    Column('trade_id', String),
    Column('order_id', String),
    Column('order_type', String),
    Column('trade_side', String),
    Column('takerormaker', String),
    Column('executed_price', REAL),
    Column('base_amount', REAL),
    Column('cost', REAL),
    Column('fee', JSON),
    Column('fees', JSON),
    Column('datetime', DATETIME),
    Column('created_at', INT, index = True)
)

table_ohlcv = Table(
    'ohlcv',
    meta,
    Column('id', Integer, primary_key = True),
    Column('exchange', String, index = True),
    Column('symbol', String, index = True),
    Column('open_price', REAL),
    Column('high_price', REAL),
    Column('low_price', REAL),
    Column('close_price', REAL),
    Column('candle_volume', REAL),
    Column('utc_timestamp', INT, index = True)
    )

table_logs = Table(
    'logs',
    meta,
    Column('id', Integer, primary_key = True),
    Column('message', String),
    Column('created_at', INT, index = True)
    )
