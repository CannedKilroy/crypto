#settings

#symbols
btc_inverse_perp = 'BTC/USD:BTC'
btc_linear_perp = 'BTC/USDT:USDT'

#ccxt settings
timeframe = '1m'
orderbook_depth = 50
timeout = 10 #seconds
complete_candles_only = True
candle_limit = 1

#storage
ob_cols = [('symbol', 'TEXT'),
           ('timestamp', 'INT'),
           ('asks', 'TEXT'),
           ('bids', 'TEXT'),
           ('nonce', 'NULL'),
           ('datetime', 'TEXT')
           ]


ticker_cols = [('symbol', 'TEXT'),
               ('timestamp', 'INT'),
               ('ask', 'REAL'),
               ('askVolume', 'REAL'),
               ('bid', 'REAL'),
               ('bidVolume', 'REAL'),
               ('open', 'REAL'), #OHLC
               ('high', 'REAL'),
               ('low', 'REAL'),
               ('close', 'REAL'),
               ('vwap', 'REAL'),
               ('previousClose', 'REAL'),
               ('change', 'REAL'),
               ('percentage', 'REAL'),
               ('average', 'REAL'),
               ('baseVolume', 'REAL'),
               ('quoteVolume', 'REAL'),
               ('last', 'REAL'),
               ('info', 'text'), #the original non-modified unparsed reply from exchange API
               ('datetime', 'TEXT')
               ]

trade_cols = [('symbol', 'TEXT'),
              ('timestamp', 'INT'),
              ('id', 'TEXT'),
              ('order_id', 'TEXT'), #order is reserved name
              ('type', 'TEXT'),
              ('side', 'Text'),
              ('takerorMaker', 'TEXT'),
              ('price', 'REAL'),
              ('amount', 'REAL'),
              ('cost', 'REAL'), #convert to real from scientific
              ('info', 'TEXT'),
              ('datetime', 'TEXT')
              ]

ohlcv_cols = [('symbol', 'TEXT'),
              ('timestamp', 'INT'),
              ('open', 'REAL'),
              ('high', 'REAL'),
              ('low', 'REAL'),
              ('close', 'REAL'),
              ('volume', 'REAL')
              ]

logs_cols = [('timestamp', 'INT'),
             ('message', 'TEXT')
             ]

tables = {
    'ticker': ticker_cols,
    'ohlcv': ohlcv_cols,
    'trades': trade_cols,
    'orderbook': ob_cols,
    'logs': logs_cols
}