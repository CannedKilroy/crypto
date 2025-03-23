from datetime import datetime
from redis_om import JsonModel, Field, get_redis_connection
from redis_om import Field as RedisField
from typing import Optional, List, Dict, Tuple, Any, Union

redis = get_redis_connection(
    host="localhost",
    port=6379,
    password=None,
    decode_responses=True
)

class Orderbook(JsonModel):
    exchange: str = RedisField(index=True)
    symbol: str = RedisField(index=True)
    
    # Standard L2 Aggregated, L3 No Aggregation, L2 Aggregated with Counts, L3 with Timestamp
    # [Price, Amount],[Price, Amount, id], [Price, Amount, Count], [Price, Amount, Timestamp]
    asks: List[Union[Tuple[float, float], Tuple[float, float, int]]] = RedisField(index=False)
    bids: List[Union[Tuple[float, float], Tuple[float, float, int]]] = RedisField(index=False)
    nonce: Optional[int] = RedisField(index=False, default=None)

    date_time: datetime = RedisField(index=False)
    created_at: int = RedisField(index=False)

    class Meta:
        database = redis

class Ticker(JsonModel):
    exchange: str = RedisField(index=True)
    symbol: str = RedisField(index=True)

    #ask: Optional[float] = RedisField(index=False)
    #ask_volume: Optional[float] = RedisField(index=False)
    #bid: Optional[float] = RedisField(index=False)
    #bid_volume: Optional[float] = RedisField(index=False)
    open_24h: Optional[float] = RedisField(index=False)
    high_24h: Optional[float] = RedisField(index=False)
    low_24h: Optional[float] = RedisField(index=False)
    close_24h: Optional[float] = RedisField(index=False)
    #last_price: Optional[float] = RedisField(index=False)
    vwap: Optional[float] = RedisField(index=False)
    #previous_close_price: Optional[float] = RedisField(index=False)
    price_change: Optional[float] = RedisField(index=False)
    percentage_change: Optional[float] = RedisField(index=False)
    average_price: Optional[float] = RedisField(index=False)
    base_volume: Optional[float] = RedisField(index=False)
    quote_volume: Optional[float] = RedisField(index=False)
    # info: dict = RedisField(index=False)

    date_time: datetime = RedisField(index=False)
    created_at: int = RedisField(index=False)

    class Meta:
        database = redis

class Trades(JsonModel):
    exchange: str = RedisField(index=True)
    symbol: str = RedisField(index=True)

    trade_id: Optional[str] = RedisField(index=False, default=None)
    order_id: Optional[str] = RedisField(index=False, default=None)
    order_type: Optional[str] = RedisField(index=True, default=None)
    trade_side: Optional[str] = RedisField(index=True, default=None)
    taker_maker: Optional[str] = RedisField(index=True, default=None)
    executed_price: float = RedisField(index=False)
    base_amount: float = RedisField(index=False)
    cost: Optional[float] = RedisField(index=False, default=None)
    fee: Optional[Dict[str, float]] = RedisField(index=False, default=None)
    fees: Optional[Dict[str, float]] = RedisField(index=False, default=None)
    # info: dict = RedisField(index=False)

    date_time: datetime = RedisField(index=False)
    created_at: int = RedisField(index=False)

    class Meta:
        database = redis

class OHLCV(JsonModel):
    exchange: str = RedisField(index=True)
    symbol: str = RedisField(index=True)

    open_price: Optional[float] = RedisField(index=False)
    high_price: Optional[float] = RedisField(index=False)
    low_price: Optional[float] = RedisField(index=False)
    close_price: Optional[float] = RedisField(index=False)
    candle_volume: Optional[float] = RedisField(index=False)

    # OHLCV does not have date time
    date_time: Optional[datetime] = RedisField(index=False, default=None)
    created_at: int = RedisField(index=False)
    
    class Meta:
        database = redis

if __name__ == "__main__":
    pass