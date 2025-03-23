'''
------------------------------------------------------------------------------------------------------------------------
Example websocket outputs from ccxt.
Trades:
[
    {
        'info':          { ... },                  // the original decoded JSON as is
        'id':           '12345-67890:09876/54321', // string trade id
        'timestamp':     1502962946216,            // Unix timestamp in milliseconds
        'datetime':     '2017-08-17 12:42:48.000', // ISO8601 datetime with milliseconds
        'symbol':       'ETH/BTC',                 // symbol
        'order':        '12345-67890:09876/54321', // string order id or undefined/None/null
        'type':         'limit',                   // order type, 'market', 'limit' or undefined/None/null
        'side':         'buy',                     // direction of the trade, 'buy' or 'sell'
        'takerOrMaker': 'taker',                   // string, 'taker' or 'maker'
        'price':         0.06917684,               // float price in quote currency
        'amount':        1.5,                      // amount of base currency
        'cost':          0.10376526,               // total cost, `price * amount`,
        'fee':           {                         // if provided by exchange or calculated by ccxt
            'cost':  0.0015,                       // float
            'currency': 'ETH',                     // usually base currency for buys, quote currency for sells
            'rate': 0.002,                         // the fee rate (if available)
        },
        'fees': [                                  // an array of fees if paid in multiple currencies
            {                                      // if provided by exchange or calculated by ccxt
                'cost':  0.0015,                   // float
                'currency': 'ETH',                 // usually base currency for buys, quote currency for sells
                'rate': 0.002,                     // the fee rate (if available)
            },
        ]
    },
    ...
]
--------------------------------------------------------------------------------------------------------------------------
Order book:
{
    'bids': [
        [ price, amount ], // [ float, float ]
        [ price, amount ],
        ...
    ],
    'asks': [
        [ price, amount ],
        [ price, amount ],
        ...
    ],
    'symbol': 'ETH/BTC', // a unified market symbol
    'timestamp': 1499280391811, // Unix Timestamp in milliseconds (seconds * 1000)
    'datetime': '2017-07-05T18:47:14.692Z', // ISO8601 datetime string with milliseconds
    'nonce': 1499280391811, // an increasing unique identifier of the orderbook snapshot
}
--------------------------------------------------------------------------------------------------------------------------
OHLCV:
[
    [
        1504541580000, // UTC timestamp in milliseconds, integer
        4235.4,        // (O)pen price, float
        4240.6,        // (H)ighest price, float
        4230.0,        // (L)owest price, float
        4230.7,        // (C)losing price, float
        37.72941911    // (V)olume float (usually in terms of the base currency, the exchanges docstring may list whether quote or base units are used)
    ],
    ...
]
--------------------------------------------------------------------------------------------------------------------------
Ticker:
{'ask': 31387.0,
 'askVolume': 260928.0,
 'average': 30843.0,
 'baseVolume': 1109194605.0,
 'bid': 31386.5,
 'bidVolume': 452330.0,
 'change': 1088.0,
 'close': 31387.0,
 'datetime': '2023-07-14T05:23:08.717Z',
 'high': 31869.0,
 'info': {'ask1Price': '31387.00',
          'ask1Size': '260928',
          'bid1Price': '31386.50',
          'bid1Size': '452330',
          'fundingRate': '0.0001',
          'highPrice24h': '31869.00',
          'indexPrice': '31391.36',
          'lastPrice': '31387.00',
          'lowPrice24h': '30283.00',
          'markPrice': '31386.50',
          'nextFundingTime': '1689321600000',
          'openInterest': '557635538',
          'openInterestValue': '17766.73',
          'prevPrice1h': '31431.00',
          'prevPrice24h': '30299.00',
          'price24hPcnt': '0.035908',
          'symbol': 'BTCUSD',
          'tickDirection': 'PlusTick',
          'turnover24h': '35713.7539',
          'volume24h': '1109194605'},
 'last': 31387.0,
 'low': 30283.0,
 'open': 30299.0,
 'percentage': 3.5908,
 'previousClose': None,
 'quoteVolume': 35713.7539,
 'symbol': 'BTC/USD:BTC',
 'timestamp': 1689312188717,
 'vwap': 3.2197915261226e-05}
 
--------------------------------------------------------------------------------------------------------------------------
Ticker:
{
    'symbol':        string symbol of the market ('BTC/USD', 'ETH/BTC', ...)
    'info':        { the original non-modified unparsed reply from exchange API },
    'timestamp':     int (64-bit Unix Timestamp in milliseconds since Epoch 1 Jan 1970)
    'datetime':      ISO8601 datetime string with milliseconds
    'high':          float, // highest price
    'low':           float, // lowest price
    'bid':           float, // current best bid (buy) price
    'bidVolume':     float, // current best bid (buy) amount (may be missing or undefined)
    'ask':           float, // current best ask (sell) price
    'askVolume':     float, // current best ask (sell) amount (may be missing or undefined)
    'vwap':          float, // volume weighed average price
    'open':          float, // opening price
    'close':         float, // price of last trade (closing price for current period)
    'last':          float, // same as `close`, duplicated for convenience
    'previousClose': float, // closing price for the previous period
    'change':        float, // absolute change, `last - open`
    'percentage':    float, // relative change, `(change/open) * 100`
    'average':       float, // average price, `(last + open) / 2`
    'baseVolume':    float, // volume of base currency traded for last 24 hours
    'quoteVolume':   float, // volume of quote currency traded for last 24 hours
}

--------------------------------------------------------------------------------------------------------------------------
Timestmaps:
exchange.parse8601 ('2018-01-01T00:00:00Z') == 1514764800000 // integer, Z = UTC
exchange.iso8601 (1514764800000) == '2018-01-01T00:00:00Z'   // iso8601 string
exchange.seconds ()      // integer UTC timestamp in seconds
exchange.milliseconds () // integer UTC timestamp in milliseconds
'''