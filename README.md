Simple python script that captures bybit websocket data for bitcoin futures, using ccxt, to a sqlite3 file, using the builtin rate limiting.

TODO:
- dictionary to make a relation between websocket response keys and table columns.
Some websocket response keys are reserved in sqlite3 so column names may be different
- function to check if a column is a reserved keyword in sqlite3
- function that translates bybit symbol to ccxt symbol
- 
