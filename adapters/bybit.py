from pybit.unified_trading import HTTP
import json
class Bybit:
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize connection to Bybit API.
        
        Args:
            api_key (str): Bybit API key
            api_secret (str): Bybit API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = self._connect()

    def _connect(self) -> HTTP:
        """
        Create connection to Bybit API.
        
        Returns:
            HTTP: Initialized Bybit client session
        """
        return HTTP(
            testnet=False,
            api_key=self.api_key,
            api_secret=self.api_secret
        )

    def reconnect(self):
        """Reconnect to Bybit API if connection is lost."""
        self.session = self._connect()

        
    def fetch_prices(self, symbols: list[str]) -> dict[str, float]:
        """
        Fetch the last traded prices for multiple trading pairs on Bybit.
        
        Args:
            symbols (list[str]): List of trading pair symbols (e.g. ['BTCUSDT', 'ETHUSDT'])
            
        Returns:
            dict[str, float]: Dictionary mapping symbols to their last traded prices.
                             Symbols that failed to fetch will be omitted.
        """
        prices = {}
        for symbol in symbols:
            try:
                ticker = self.session.get_tickers(
                    category="spot",
                    symbol=symbol  # Pass single symbol instead of joined string
                )
                
                price = float(ticker['result']['list'][0]['lastPrice'])
                prices[symbol] = price
                
            except Exception as e:
                print(f"Error fetching price for {symbol} from Bybit: {str(e)}")
                continue

        return prices

    def fetch_balance(self) -> float:
        """
        Fetch total account balance from Bybit.
        
        Returns:
            float: Total account balance in USD
        """
        try:
            # Get wallet balance
            balance = self.session.get_wallet_balance(
                accountType="UNIFIED"
            )
            
            # Calculate total balance
            total = 0
            for coin in balance['result']['list'][0]['coin']:
                total += float(coin['usdValue'])
                
            return total
            
        except Exception as e:
            print(f"Error fetching balance from Bybit: {str(e)}")
            return None

def fetch_bybit_price(symbol):
    """
    Fetch the last traded price for a given trading pair on Bybit.
    
    Args:
        symbol (str): Trading pair symbol (e.g. 'BTCUSDT')
        
    Returns:
        float: Last traded price, or None if error
    """
    try:
        # Load API credentials from config
        with open('config.json') as f:
            config = json.load(f)
            api_key = config['bybit']['api_key']
            api_secret = config['bybit']['api_secret']

        # Initialize Bybit client
        session = HTTP(
            testnet=False,
            api_key=api_key,
            api_secret=api_secret
        )
        
        # Get latest ticker price
        ticker = session.get_tickers(
            category="spot",
            symbol=symbol
        )
        
        # Return last price
        return float(ticker['result']['list'][0]['lastPrice'])
        
    except Exception as e:
        print(f"Error fetching {symbol} price from Bybit: {str(e)}")
        return None


def fetch_bybit_balance():
    # Load API credentials from config
    with open('config.json') as f:
        config = json.load(f)
        api_key = config['bybit']['api_key']
        api_secret = config['bybit']['api_secret']

    # Initialize Bybit client
    session = HTTP(
        testnet=False,
        api_key=api_key,
        api_secret=api_secret
    )

    try:
        # Fetch wallet balance
        response = session.get_wallet_balance(
            accountType="UNIFIED",
        )

        # Extract total balance in USD
        total_balance = float(response['result']['list'][0]['totalEquity'])
        return total_balance

    except Exception as e:
        print(f"Error fetching Bybit balance: {str(e)}")
        return 0
