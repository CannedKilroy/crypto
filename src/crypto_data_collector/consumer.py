"""
TODO:
- Figure out naming convention for s3?
- Save as parquet?
- Time or size based batch?
( Size as that is the actual constraint but python is funny w size => time)
- Compress data? Layer compression?
- Individual stream condition for dumping on random

Uses the same naming scheme as redis
Exchange:Symbol:Stream
"""

import asyncio

class Consumer:
    def __init__(self, consumer_config:dict):
        self.archival_batch = []
        self.consumer_config = consumer_config
        self.start_time = None
        self.time_window = int(300) # 300 seconds ie 5 min
        
    async def consumer_delegator(self, config:dict, data_queue:asyncio.Queue):    
        while True:
            full_data = await data_queue.get()
            #await self.archival_batch(full_data)
            await self.redis_consumer(full_data)

    async def redis_consumer(self, full_data:dict):
        # Use redis ordered set
        # No do not, cannot store nested json
        # Redis ts: No, only takes in value value: Union[int, float]
        # Can serialize data
        # Use redisjson
        # No, use redis streams that supports
        # event driven pub sub model. Messages are stored with TTL
        # But it cannot support nested json sooo back to redisjson
        # Just us redis OM since it does all this shit
        cleaned_data = self._data_cleaner(full_data)
        exchange_name, symbol_name, stream_name = cleaned_data["key_str"].split("*")
        #, room=f"{exchange_name}/{symbol_name}
        print("\ncleaned_data")
        print(cleaned_data)
        #socketio.emit("crypto_data", cleaned_data, broadcast=True)


        if stream_name == "watchOrderBook":
            ob = Orderbook(
                    exchange = exchange_name,
                    symbol = symbol_name,
                    asks = cleaned_data["asks"],
                    bids = cleaned_data["bids"],
                    nonce = cleaned_data["nonce"],
                    date_time = cleaned_data["datetime"],
                    created_at = cleaned_data["timestamp"]
                    )
            ob.save()
            ob.expire(self.time_window)

        elif stream_name == "watchTrades":
            trade = Trades(
                    exchange = exchange_name,
                    symbol = symbol_name,

                    order_type = cleaned_data["type"],
                    trade_side = cleaned_data["side"],
                    taker_maker = cleaned_data["takerOrMaker"],
                    executed_price = cleaned_data["price"],
                    base_amount = cleaned_data["amount"],

                    date_time = cleaned_data["datetime"],
                    created_at = cleaned_data["timestamp"]
                    )
            trade.save()
            trade.expire(self.time_window)

        elif stream_name == "watchTicker":
            ticker = Ticker(
                    exchange = exchange_name,
                    symbol = symbol_name,

                    open_24h = cleaned_data["open"],
                    high_24h = cleaned_data["high"],
                    low_24h = cleaned_data["low"],
                    close_24h = cleaned_data["close"],
                    vwap = cleaned_data["vwap"],
                    price_change = cleaned_data["change"],
                    average_price = cleaned_data["average"],
                    base_volume = cleaned_data["baseVolume"],
                    quote_volume = cleaned_data["quoteVolume"],
                    percentage_change = cleaned_data["percentage"],

                    date_time = cleaned_data["datetime"],
                    created_at = cleaned_data["timestamp"]
                    )
            ticker.save()
            ticker.expire(self.time_window)
        
        elif stream_name == "watchOHLCV":
            ohlcv = OHLCV(
                    exchange = exchange_name,
                    symbol = symbol_name,

                    open_price = cleaned_data["candle_open"],
                    high_price = cleaned_data["candle_high"],
                    low_price = cleaned_data["candle_low"],
                    close_price = cleaned_data["candle_close"],
                    candle_volume = cleaned_data["candle_volume"],
                    date_time = None,
                    created_at = cleaned_data["timestamp"]
                    )
            ohlcv.save()
            ohlcv.expire(self.time_window)


    async def archival_consumer(self, data:dict):
        symbol_name, stream_name, key_str, data, time_receive = data.values()

        if stream_name not in self.consumer_config['archival_storage']['valid_streams']:
            return None
        
        # Batch Empty
        if self.archival_batch == []:
            clean_data = self._data_cleaner(data)
            self.archival_batch.append(clean_data)
            self.start_time = clean_data["timestamp"]
        # Within time window, append
        elif time_receive - self.archival_batch[0] < self.time_window:
            clean_data = self._data_cleaner(data)
            self.archival_batch.append(clean_data)
        # Batch full
        elif time_receive - self.archival_batch[0] >= self.time_window:
            self._archival_data_writer(self.archival_batch)
    
    def _data_cleaner(self, data):
        """ Cleans Data for Archival"""
        symbol_name, stream_name, key_str, data, time_receive = data.values()

        # Move into config
        OHLCV_keys = [] # Build OHLCV, not all have the endpoint?
        orderbook_keys = ["datetime", "bids", "asks", "timestamp", "nonce"]
        trades_keys = ["datetime","timestamp", "type", "side", "takerOrMaker", "price", "amount"]
        ticker_keys = [
            "average", "baseVolume", "change",
             "close", "datetime", "high",
             "last", "low", "open", "vwap", 
             "percentage", "quoteVolume", "timestamp"
             ]
        
        cleaned_data = {}
        if stream_name == "watchOrderBook":
            for key, value in data.items():
                if key in orderbook_keys:
                    cleaned_data[key] = data[key]
            cleaned_data["key_str"] = key_str
        elif stream_name == "watchTrades":
            for key, value in data[0].items():
                if key in trades_keys:
                    cleaned_data[key] = data[0][key]
            cleaned_data["key_str"] = key_str
        elif stream_name == "watchTicker":
            for key, value in data.items():
                if key in ticker_keys:
                    cleaned_data[key] = data[key]
            cleaned_data["key_str"] = key_str
        elif stream_name == "watchOHLCV":
            cleaned_data["timestamp"] = data[-1][0]
            cleaned_data["candle_open"] = data[-1][1]
            cleaned_data["candle_high"] = data[-1][2]
            cleaned_data["candle_low"] = data[-1][3]
            cleaned_data["candle_close"] = data[-1][4]
            cleaned_data["candle_volume"] = data[-1][5]
            cleaned_data["key_str"] = key_str
        return cleaned_data
    
    async def _archival_data_writer(self, data):
        # Write data to archive
        pass