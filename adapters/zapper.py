import requests
from typing import Dict, Any
import base64

query = """
query ($addresses: [Address!]!) {
  portfolio(addresses: $addresses) {
    totals {
      total
      totalWithNFT
    }
  }
}
"""

def fetch_zapper_balance(addresses, api_key) -> Dict[str, Any]:
    encoded_zapper_key = base64.b64encode(api_key.encode()).decode()
    print(f"Loading portfolio for {addresses}")
    try:
        response = requests.post(
            'https://public.zapper.xyz/graphql',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_zapper_key}'
            },
            json={
                'query': query,
                'variables': {
                    'addresses': addresses,
                }
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        if 'errors' in data:
            raise ValueError(f"GraphQL Errors: {data['errors']}")

        return data['data']

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        raise
    except ValueError as e:
        print(f"Data validation failed: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise