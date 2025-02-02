import psycopg
from psycopg.rows import dict_row

class PortfolioDatabase:
    def __init__(self, dbname, user, password, host, port):
        """
        Initializes the database connection and sets up the cursor.
        """
        try:
            self.connection = psycopg.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            raise

    def save_balances(self, snapshot_time, balances):
        """
        Inserts multiple balance entries into the balances table.

        Args:
        - snapshot_time (datetime): The timestamp for all entries in this batch.
        - balances (list of tuples): Each tuple contains (source, usd_value).

        Example:
        save_balances(datetime.now(), [('SourceA', 100.50), ('SourceB', 200.75)])
        """
        insert_query = """
        INSERT INTO balances (snapshot_time, source, usd_value)
        VALUES %s;
        """
        # Prepare data for batch insertion
        data = [(snapshot_time, source, usd_value) for source, usd_value in balances]

        try:
            # psycopg v3 handles batch inserts differently
            self.cursor.executemany(
                "INSERT INTO balances (snapshot_time, source, usd_value) VALUES (%s, %s, %s)",
                data
            )
            self.connection.commit()
            print(f"{len(balances)} entries saved successfully.")
        except Exception as e:
            print(f"Failed to insert balances: {e}")
            self.connection.rollback()
            raise

    def save_prices(self, snapshot_time, prices):
        """
        Inserts multiple price entries into the prices table.

        Args:
        - snapshot_time (datetime): The timestamp for all entries in this batch.
        - prices (list of tuples): Each tuple contains (pair, base_currency, quote_currency, price).

        Example:
        save_prices(datetime.now(), [
            ('ETH/USDT', 'ETH', 'USDT', 1850.45),
            ('BTC/USDT', 'BTC', 'USDT', 26500.00),
            ('USD/AUD', 'USD', 'AUD', 1.52)
        ])
        """
        insert_query = """
        INSERT INTO prices (snapshot_time, pair, base_currency, quote_currency, price)
        VALUES (%s, %s, %s, %s, %s);
        """
        # Prepare data for batch insertion
        data = [(snapshot_time, x['ticker'], x['base'], x['quote'], x['price'])
                for x in prices]

        try:
            self.cursor.executemany(
                insert_query,
                data
            )
            self.connection.commit()
            print(f"{len(prices)} price entries saved successfully.")
        except Exception as e:
            print(f"Failed to insert prices: {e}")
            self.connection.rollback()
            raise


    def close(self):
        """
        Closes the database connection and cursor.
        """
        try:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
        except Exception as e:
            print(f"Failed to close the database: {e}")
