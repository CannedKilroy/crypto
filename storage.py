#datastorage
import sqlite3
import pprint

class ConnectionManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(f"{self.db_name}.db")

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()


class Database:
    def __init__(self, db_name:str):
        """
        Creates Database object using sqlite3

        :param db_name: Name of the database.
        """
        
        self.db_name = db_name
        self.connection_manager = ConnectionManager(db_name)
        
        #cache table names and columns        
        self.tables = {}
        
        #connect to database, create if it doesnt exist
        self.connection_manager.connect()
        print(f"Connected or created {self.db_name} database\n")
    
    def _table_exists(self, table_name:str):
        """
        Check if a table exists in the database

        :param table_name: Name of the table
        :return: True if the table exists, False otherwise.
        """
        with self.connection_manager.conn:
            c = self.connection_manager.conn.cursor()
            
            c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (str(table_name),))
            count = c.fetchone()[0]
            
            return count == 1
            
    def parse_object(self, obj):
        '''
        Returns equivalent sqlite3 object type from python type.

        :param obj: Object type to be converted
        '''
        if type(obj) is str:
            return 'TEXT'
        if type(obj) is int:
            return 'INTEGER'
        if type(obj) is float:
            return 'REAL'
        if type(obj) is list:
            return json.dumps(obj)
        print(type(object))
        return 'TEXT'
        
    def create_table(self, table_name:str, columns:list, drop_table = False, primary_key = None):
        """
        Create a table

        :param table_name: Name of the table
        :param columns: List of tuples in (column_name, data_type) format for the columns
        :param drop_table: Whether to drop the table if it exists
        :param primary_key: Which column is the primary key
        """
        with self.connection_manager.conn:
            c = self.connection_manager.conn.cursor()
            
            if self._table_exists(table_name) == False:
                print('Table does not exist')
            elif drop_table:
                c.execute(f'''DROP TABLE IF EXISTS {table_name}''')
                print(f"Existing table {table_name} was dropped")
            else:
                print(f"Table {table_name} already exists")
                return
            
            self.tables[table_name] = [column for column, _ in columns]

            print(f"Creating table {table_name}")
            
            column_definitions = ', '.join([f"{column} {data_type}" for column, data_type in columns])
            create_table_query = f"CREATE TABLE {table_name} ({column_definitions}"
            
            if primary_key:
                create_table_query += f", PRIMARY KEY ({primary_key})"
            if unique:
                create_table_query += ', UNIQUE(' + ', '.join(name for name, _ in columns) + ')'
                
            create_table_query += ")"
            try:
                c.execute(create_table_query)
            except Exception as e:
                raise e
            
            print(f"Table '{table_name}' created\n")
    
    def insert_one(self, table_name:str, data:tuple):
        """
        Insert one row into a table

        :param table_name: Name of the table
        :param data: Data to be inserted
        """
        with self.connection_manager.conn:
            c = self.connection_manager.conn.cursor()
        
            if self._table_exists(table_name) == False:
                raise Exception("Table Does not exist")
            
            columns = self.tables[table_name]
            
            wildcard = ', '.join(['?'for _ in columns])
            _= '?,'*len(columns)
            string_holder = _[0:-1]
            
            try:
                command = f"INSERT INTO {table_name} {tuple(columns)} VALUES ({wildcard})"
                c.execute(command,data)
            except Exception as e:
                raise e
    
    def return_all(self, table_name:str):
        """
        Return all data from a table

        :param table_name: Name of the table
        :return: List of rows
        """
        with self.connection_manager.conn:
            c = self.connection_manager.conn.cursor()
            
            if self._table_exists(table_name) == False:
                raise Exception("Table Does not exist")
            
            c.execute(f"SELECT ROWID,* FROM {table_name}")
            items = c.fetchall()
            for item in items:
                print(item)
            return items
            
    def execute_cmd(self, command:str):
        """
        Execute a raw SQL command

        :param command: Command to be executed
        """
        with self.connection_manager.conn:
            c = self.connection_manager.conn.cursor()
            try:
                c.execute(command)
            except Exception as e:
                raise e

    def drop_table(self):
        #TODO
        pass
    
    def insert_many(self):
        #TODO
        pass
    
    def select_n(self, table_name:str, condition:str):
        #TODO
        pass        
    
    

if __name__ == "__main__":
    # Create db and tables
    db = Database('test')

    # Create table 'orderbook'
    orderbook_columns = [
        ('asks', 'TEXT'),
        ('bids', 'TEXT'),
        ('datetime', 'TEXT'),
        ('nonce', 'INTEGER'),
        ('symbol', 'TEXT'),
        ('timestamp', 'INTEGER')
    ]
    db.create_table(table_name='orderbook', columns=orderbook_columns, drop_table=True)

    # Test inserting data into 'orderbook'
    data = (
        str([[30271.5, 59512.0], [30272.0, 16904.0], [30273.0, 3211.0]]),
        str([[30271.0, 536680.0], [30270.5, 19991.0], [30270.0, 55217.0]]),
        '2023-07-17T06:25:04.554Z',
        None,
        'BTC/USD:BTC',
        1689575104554
    )
    db.insert_one(table_name='orderbook', data=data)
    db.insert_one(table_name='orderbook', data=data)

    # Return all rows from 'orderbook'
    items = db.return_all(table_name='orderbook')
    print(items)
    print('Success!')
    
