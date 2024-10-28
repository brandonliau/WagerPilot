# Local imports
from wagerpilot.tools.config_utils import Config
# Third party imports
import requests

def get_sports(config: Config) -> list:
    token, prev_usage = config.get_token()
    base_url = 'https://api.the-odds-api.com/v4/sports/'
    params = {
        'apiKey': token,
    }
    resp = requests.get(base_url, params=params)
    config.update_usage(token, prev_usage, int(resp.headers['X-Requests-Remaining']))
    return resp.json()

def get_events(config: Config, sport: str, market: str) -> list:
    token, prev_usage = config.get_token()
    base_url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds'
    params = {
        'apiKey': token,
        'bookmakers': config.bookies_string,
        'markets': market,
        'oddsFormat': 'decimal',
    }
    resp = requests.get(base_url, params=params)
    if resp.status_code != 200:
        return None
    config.update_usage(token, prev_usage, int(resp.headers['X-Requests-Remaining']))
    return resp.json()
