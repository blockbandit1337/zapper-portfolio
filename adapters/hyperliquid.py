from typing import List
import requests

class Hyperliquid:
    def __init__(self, target_addresses: List[str]):
        self.target_addresses = target_addresses

    def get_hype_price(self):
        try:
            response = requests.post(
                "https://api.hyperliquid.xyz/info",
                headers={
                    "accept": "*/*",
                    "content-type": "application/json",
                },
                json={
                    "type": "tokenDetails",
                    "tokenId": "0x0d01dc56dcaaca66ad901c959b4011ec"  # HYPE token ID
                }
            )
            response.raise_for_status()
            token_details = response.json()
            
            # Return the mark price (current market price)
            return float(token_details['markPx'])
            
        except Exception as e:
            print(f"Error fetching HYPE price: {str(e)}")
            return 0
    
    def fetch_staked_hype(self):
        address_to_amount = {}
        for address in self.target_addresses:
            try:
                response = requests.post(
                    "https://api-ui.hyperliquid.xyz/info",
                    headers={
                        "accept": "*/*",
                        "accept-language": "en-US,en;q=0.9",
                        "content-type": "application/json",
                    },
                    json={
                        "type": "delegations",
                        "user": address
                    }
                )
                response.raise_for_status()
                delegations = response.json()
                print("hyperliquid staking")
                print(delegations)
                
                # Sum up all delegation amounts for this address
                total_amount = sum(float(delegation['amount']) for delegation in delegations)
                address_to_amount[address] = total_amount
                
            except Exception as e:
                print(f"Error fetching staked HYPE for address {address}: {str(e)}")
                address_to_amount[address] = 0  # Set to 0 if there's an error
                continue
        
        return address_to_amount
    
    def fetch_hype_balances(self):
        address_to_amount = {}
        for address in self.target_addresses:
            try:
                response = requests.post(
                    "https://api-ui.hyperliquid.xyz/info",
                    headers={
                        "accept": "*/*",
                        "accept-language": "en-US,en;q=0.9",
                        "content-type": "application/json",
                    },
                    json={
                        "type": "spotClearinghouseState",
                        "user": address
                    }
                )
                response.raise_for_status()
                balances = response.json()
                print("hyperliquid spot balances")
                print(balances)

                total_amount = 0.0
                for token in balances["balances"]:
                    if token["coin"] == "HYPE":
                        total_amount += float(token["total"])
                
                # Sum up all delegation amounts for this address
                # total_amount = sum(float(tokens['amount']) for tokens in balances)
                address_to_amount[address] = total_amount
                
            except Exception as e:
                print(f"Error fetching staked HYPE for address {address}: {str(e)}")
                address_to_amount[address] = 0  # Set to 0 if there's an error
                continue
        
        return address_to_amount
    
    def get_total_usd_balance(self):
        hype_price = self.get_hype_price()
        total_usd = 0
        staked_hype = self.fetch_staked_hype()
        spot_hype = self.fetch_hype_balances()
        for hype in staked_hype.values():
            total_usd += hype * hype_price
        
        for hype in spot_hype.values():
            total_usd += hype * hype_price
        
        return total_usd
