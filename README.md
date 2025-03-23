![Alt Text](https://github.com/CannedKilroy/crypto/blob/main/Assets/ccxt_resize.png)
# Cryptocurrency Futures Data Capture Tool

## Introduction
A python-based data pipeline that uses the CCXT and SQLAlchemy libraries to asynchronously capture and store real-time cryptocurrency exchange data. It uses CCXT WebSocket streams and feeds the data into a MySQL database. Designed to support multiple exchanges / tickers simultaneously and is compatible with all CCXT-supported exchanges.

It is not suitable for realtime trading. It's intended for gathering reatlime data for backtesting / research, an alternative to expensive 3rd party data providers. 

## Dependencies
- Python 3.11 or newer
- SQLalchemy
- MySQL
- CCXT
- Poetry

## Setup
- Install Poetry
  - Poetry is required to handle dependencies and create a virtual env for this project. If you don't have Poetry installed, install it by following the [official Poetry installation guide](https://python-poetry.org/docs/#installation).
- Clone repo to local machine
  - `git clone https://github.com/CannedKilroy/crypto.git`
- Open directory
  - `cd crypto`
- Install dependencies
  - `poetry install`
- Edit `config` file inside `config/` for database credentials, the exchanges / symbols you want, etc. The CCXT symbol naming conventions can be found [here](https://docs.ccxt.com/#/?id=contract-naming-conventions)

## Usage
- `poetry run python src/main.py`

## DB Diagram
![Alt Text](https://github.com/CannedKilroy/crypto/blob/main/Assets/crypto_websocket_stream_resized.png)
The streams that are captured:
- OHLCV
- ticker information
- time and sales (recent trades)
- order book
Alongside any exceptions

The original JSON reponse from the exchange is kept as well, as depending on the exchange, sometimes CCXT doesn't keep all the orignal info. 

## Note
A single inverse bitcoin futures contract generates approximatly ~15-35 gigabytes of data a day.

### TODO:
- Fix issue with exchanges timing out when loading markets. Load markets with the exchange loop.
- Allow for variable keyowrd args in exchange loop, so user can additional args if needed such as timeout etc.
- Switch to logging
- Add Apache Airflow
- Send heartbeat more often so exchange doesnt timeout when market is very active.
- Switch to time series DB
- DB normalization

## Links used:
- https://github.com/ccxt/ccxt/blob/master/examples/ccxt.pro/py/one-exchange-different-streams.py
- https://docs.ccxt.com/#/?id=error-handling
- https://github.com/ccxt/ccxt/blob/master/examples/ccxt.pro/py/build-ohlcv-many-symbols.py
