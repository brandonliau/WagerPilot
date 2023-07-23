# Third party imports
from pymongo import MongoClient
# Local imports
import wagerpilot.config as con
import wagerpilot.support.bookmakers as bookie

def retrieveSports():
    client = MongoClient(con.mongoConnectionString)
    collection = client['WagerSports']['activeSports']
    data = {}
    for item in collection.find({}):
        data.append(item['key'])
    return data

def parseOdds(event: dict, homeTeam: str, awayTeam: str) -> dict:
    homeOdds, awayOdds, drawOdds = {}, {}, {}
    draw = False
    for bookie in event['bookmakers']:
        for market in bookie['markets']:
            for outcome in market['outcomes']:
                bookieKey = bookie['key']
                if outcome['name'] == homeTeam:
                    homeOdds[bookieKey] = outcome['price']
                elif outcome['name'] == awayTeam:
                    awayOdds[bookieKey] = outcome['price']
                elif outcome['name'] == 'Draw':
                    draw = True
                    drawOdds[bookieKey] = outcome['price']
    if draw:
        return [homeOdds, awayOdds, drawOdds]
    return [homeOdds, awayOdds]

def findBestOdds(odds: dict):
    regions = ['best'] + list(set(map(lambda x: bookie.bmap[x], odds.keys())))
    temp = dict.fromkeys(regions, [])
    largest = dict.fromkeys(regions, 0)
    largestOverall = 0 
    for k,v in odds.items():
        if v > largestOverall:
            largestOverall = v
            temp['best'] = [v, k]
        elif v == largestOverall:
            temp['best'].append(k)
        if v > largest[bookie.bmap[k]]:
            largest[bookie.bmap[k]] = v
            temp[bookie.bmap[k]] = [v, k]
        elif v == largest[bookie.bmap[k]]:
            temp[bookie.bmap[k]].append(k)
    return temp