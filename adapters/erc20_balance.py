from web3 import Web3
from typing import Dict, Any

# Standard ERC20 ABI for balanceOf function
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }
]

class BalanceFetcher:
    def __init__(self, web3_connection: Web3):
        """
        Initialize the BalanceFetcher with a Web3 connection.
        
        Args:
            web3_connection (Web3): An established Web3 connection
        """
        self.w3 = web3_connection

    def get_token_balance(self, token_address: str, wallet_address: str) -> Dict[str, Any]:
        """
        Fetch the balance of a specific ERC20 token for a given wallet address.
        
        Args:
            token_address (str): The address of the ERC20 token contract
            wallet_address (str): The wallet address to check the balance for
            
        Returns:
            Dict containing:
                - raw_balance: The raw balance as returned by the contract
                - address: The token contract address
                - wallet: The wallet address checked
        """
        try:
            # Create the contract instance
            token_contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(token_address),
                abi=ERC20_ABI
            )
            
            # Get the balance
            balance = token_contract.functions.balanceOf(
                self.w3.to_checksum_address(wallet_address)
            ).call()
            
            return balance
            
        except Exception as e:
            print(f"Error fetching balance for token {token_address}: {str(e)}")
            raise
