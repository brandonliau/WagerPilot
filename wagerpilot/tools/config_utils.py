# Standard library imports
import asyncio
from dataclasses import dataclass
import yaml
# Third party imports
import aiohttp
from sortedcontainers import SortedList

@dataclass
class Config:
    bookies: list = None
    bookies_string: str = None
    markets: list = None
    tokens: SortedList = None

    async def load_config(self, filename: str):
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        tasks = [self.token_usage(i) for i in data['tokens']]
        results = await asyncio.gather(*tasks)
        self.bookies = data['bookies']
        self.bookies_string = ",".join(str(i) for i in data['bookies'])
        self.markets = data['markets']
        self.tokens = SortedList(zip(data['tokens'], results), key=lambda x: -x[1])

    async def token_usage(self, token: str) -> int:
        base_url = f'https://api.the-odds-api.com/v4/sports/?apiKey={token}'
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url) as resp:
                if resp.status != 200:
                    return 0
                return int(resp.headers.get('X-Requests-Remaining', 0))
            
    def get_token(self) -> str:
        return self.tokens[0][0], self.tokens[0][1]

    def update_usage(self, token: str, prev_usage: int, new_usage: int):
        self.tokens.remove((token, prev_usage))
        self.tokens.add((token, new_usage))
