# Standard library imports
import asyncio
import yaml
# Local imports
from wagerpilot.tools.api_utils import token_usage
# Third party imports
from sortedcontainers import SortedList

def load_config(filename: str) -> dict:
    with open(filename, 'r') as f:
        config = yaml.safe_load(f)
    config['bookies_string'] = ",".join(str(i) for i in config['bookies'])
    config['markets_string'] = ",".join(str(i) for i in config['markets'])
    config['tokens'] = SortedList(
        [(list(i.keys())[0], list(i.values())[0]) for i in config['tokens']],
        key=lambda x: -x[1]
    )
    return config

def save_config(filename: str, config: dict):
    copy = config.copy()
    del copy['bookies_string']
    del copy['markets_string']
    copy['tokens'] = [{k[0]: v} for k, v in copy['tokens']]
    with open(filename, 'w') as f:
        yaml.safe_dump(copy, f, default_flow_style=False)

async def sync_usage(config: dict):
    tasks = [token_usage(i) for i, _ in config['tokens']]
    results = await asyncio.gather(*tasks)
    tokens = []
    for i, j in zip(config['tokens'], results):
        tokens.append((i[0], j))
    config['tokens'] = SortedList(tokens, key=lambda x: -x[1])

def update_usage(config: dict, token: str, prev_usage: int, new_usage: int):
    config['tokens'].remove((token, prev_usage))
    config['tokens'].add((token, new_usage))
