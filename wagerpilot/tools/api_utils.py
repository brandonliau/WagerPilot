# Standard library imports
from typing import Tuple
# Third party imports
import aiohttp
import requests

async def token_usage(token: str) -> int:
    base_url = 'https://api.the-odds-api.com/v4/sports/'
    params = {
        'apiKey': token,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as resp:
            if resp.status != 200:
                return 0
            return int(resp.headers.get('X-Requests-Remaining', 0))
    
def sports_api(config: dict) -> Tuple[dict, int]:
    token = config['tokens'][0]
    base_url = 'https://api.the-odds-api.com/v4/sports/'
    params = {
        'apiKey': token,
    }
    resp = requests.request("GET", base_url, params=params)
    return resp.json(), int(resp.headers['X-Requests-Remaining'])

def events_api(config: dict, sport: str) -> Tuple[dict, int]:
    token = config['tokens'][0]
    base_url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds'
    params = {
        'apiKey': token,
        'bookmakers': config['bookies_string'],
        'markets': config['markets_string'],
        'oddsFormat': 'decimal',
    }
    resp = requests.Request("GET", base_url, params=params)
    return resp.json(), int(resp.headers['X-Requests-Remaining'])
