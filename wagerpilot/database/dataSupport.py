# Local imports
import wagerpilot.tools.dbUtils as db
import wagerpilot.support.bookmakers as bookie
import wagerpilot.betting.probability as prob

def retrieveSports():
    collection = db.getCollection('WagerSports', 'activeSports')
    data = []
    for item in collection.find({}, {'key':1, '_id':0}):
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

def findBest(eventOdds: dict):
    regions = ['best'] + list(set(map(lambda x: bookie.bmap[x], eventOdds.keys())))
    temp = dict.fromkeys(regions, [])
    largest = dict.fromkeys(regions, 0)
    largestOverall = 0 
    for k,v in eventOdds.items():
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

def parseArbitrage(eventOdds: dict, region: str):
    temp = {}
    homeOdds, awayOdds, drawOdds = eventOdds['home_odds'][region], eventOdds['away_odds'][region], [0]
    temp['home_odds'] = homeOdds
    temp['away_odds'] = awayOdds
    if 'draw_odds' in eventOdds and region in eventOdds['draw_odds']:
        drawOdds = eventOdds['draw_odds'][region]
        temp['draw_odds'] = drawOdds
    temp['implied_probability'] = prob.totalImpliedProbability(homeOdds[0], awayOdds[0], drawOdds[0])
    return temp