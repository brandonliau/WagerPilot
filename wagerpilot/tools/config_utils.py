# Standard library imports
import asyncio
from dataclasses import dataclass
import yaml
# Third party imports
import aiohttp
import requests
from sortedcontainers import SortedList

@dataclass
class Config:
    bookies: list = None
    bookies_string: str = None
    markets: list = None
    markets_string: str = None
    tokens: SortedList = None

    def load_config(self, filename: str):
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        self.bookies = data['bookies']
        self.bookies_string = ",".join(str(i) for i in data['bookies'])
        self.markets = data['markets']
        self.tokens = SortedList([(list(i.keys())[0], list(i.values())[0]) for i in data['tokens']], key=lambda x: -x[1])

    def save_config(self, filename: str):
        data = {
            'bookies': self.bookies,
            'markets': self.markets,
            'tokens': [{k: v} for k, v in self.tokens]
        }
        with open(filename, 'w') as f:
            yaml.safe_dump(data, f, default_flow_style=False)

    async def sync_usage(self):
        tasks = [self.__token_usage(i) for i, _ in self.tokens]
        results = await asyncio.gather(*tasks)
        temp = []
        for i, j in zip(self.tokens, results):
            temp.append((i[0], j))
        self.tokens = SortedList(temp, key=lambda x: -x[1])

    def get_sports(self) -> list:
        token, prev_usage = self.__get_token()
        base_url = 'https://api.the-odds-api.com/v4/sports/'
        params = {
            'apiKey': token,
        }
        resp = requests.get(base_url, params=params)
        self.__update_usage(token, prev_usage, int(resp.headers['X-Requests-Remaining']))
        return resp.json()
    
    def get_events(self, sport: str, market: str) -> list:
        token, prev_usage = self.__get_token()
        base_url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds'
        params = {
            'apiKey': token,
            'bookmakers': self.bookies_string,
            'markets': market,
            'oddsFormat': 'decimal',
        }
        resp = requests.get(base_url, params=params)
        self.__update_usage(token, prev_usage, int(resp.headers['X-Requests-Remaining']))
        return resp.json()

    def __get_token(self) -> str:
        return self.tokens[0][0], self.tokens[0][1]

    def __update_usage(self, token: str, prev_usage: int, new_usage: int):
        self.tokens.remove((token, prev_usage))
        self.tokens.add((token, new_usage))
    
    async def __token_usage(self, token: str) -> int:
        base_url = f'https://api.the-odds-api.com/v4/sports/?apiKey={token}'
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url) as resp:
                if resp.status != 200:
                    return 0
                return int(resp.headers.get('X-Requests-Remaining', 0))
            