from adapters.zapper import fetch_zapper_balance
from adapters.bybit import Bybit, fetch_bybit_balance, fetch_bybit_price
import json
from postgres import PortfolioDatabase
import time
from datetime import datetime, timedelta
from web3 import Web3
from adapters.fixed_balance import FixedBalance
from adapters.hyperliquid import Hyperliquid

def fetch_and_save_portfolio(config, web3_connection):

    # Fetch bybit prices
    bybit = Bybit(config['bybit']['api_key'], config['bybit']['api_secret'])
    price_tickers = [price['ticker'] for price in config['prices']]
    prices = bybit.fetch_prices(price_tickers)
    print("Bybit Prices: ", prices)

    # Format bybit prices
    price_records = []
    for price_config in config['prices']:
        ticker = price_config['ticker']
        if ticker in prices:
            price_records.append({
                'ticker': ticker,
                'base': price_config['base'], 
                'quote': price_config['quote'],
                'price': prices[ticker]
            })

    database = PortfolioDatabase(**config['postgresql'])
    try:
        # Fetch all balances needed
        zapper_wallets = config['evm_wallets'] + config['solana_wallets']
        zapper_balance = fetch_zapper_balance(
            zapper_wallets, config['zapper']['api_key'])
        bybit_balance = fetch_bybit_balance()

        hyperliquid = Hyperliquid(config['evm_wallets'])
        hyper_balance = hyperliquid.get_total_usd_balance()

        records = [
            ("zapper", zapper_balance['portfolio']['totals']['totalWithNFT']),
            ("bybit", bybit_balance),
            ('hyperliquid', hyper_balance)

        ]

        # ONLY SAVE IN PROD MODE
        if PROD:
            database.save_balances(datetime.now().replace(minute=0,
                second=0, microsecond=0), records)
            
            database.save_prices(datetime.now().replace(minute=0,
                second=0, microsecond=0), price_records)

        sum_bal = bybit_balance + zapper_balance['portfolio']['totals']['totalWithNFT'] + hyper_balance
        print("Portfolio data:")
        print(f"Bybit: {bybit_balance} USD")
        print(
            f"Zapper: {zapper_balance['portfolio']['totals']['totalWithNFT']} USD")
        print(f"Hyperliquid: {hyper_balance} USD")
        print(f"Aggregate: {sum_bal}")
        print("------------------------------------")
        print("Prices")
        print(price_records)
        print("------------------------------------")
        database.close()

    except Exception as e:
        print(f"Failed to fetch portfolio: {e}")

def run_every_eight_hours(config):
    """
    Runs the task every 8 hours (at 00:00, 08:00, and 16:00) according to system time.
    On startup, finds the next closest interval and sleeps until then.
    """
    # Initialize Web3 connection to Ethereum mainnet
    mainnet_web3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
    if not mainnet_web3.is_connected():
        raise Exception("Failed to connect to Ethereum mainnet")

    while True:
        now = datetime.now()
        # Find the next run time (either 00:00, 08:00, or 16:00)
        if now.hour < 8:
            next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
        elif now.hour < 16:
            next_run = now.replace(hour=16, minute=0, second=0, microsecond=0)
        else:
            next_run = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Time to sleep in seconds
        sleep_seconds = (next_run - now).total_seconds()
        print(f"Sleeping for {sleep_seconds:.2f} seconds until {next_run.strftime('%H:%M')}...")

        time.sleep(sleep_seconds)  # Sleep until next interval
        fetch_and_save_portfolio(config, mainnet_web3)

def run_instance(config):

    # Initialize Web3 connection to Ethereum mainnet
    mainnet_web3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
    if not mainnet_web3.is_connected():
        raise Exception("Failed to connect to Ethereum mainnet")

    print(
        f"Running a single instance for development purposes")

    fetch_and_save_portfolio(config, mainnet_web3) 


if __name__ == "__main__":
    config = json.load(open('config.json'))

    PROD = config.get('prod', False)
    if PROD:
        run_every_eight_hours(config)
    else:
        run_instance(config)
