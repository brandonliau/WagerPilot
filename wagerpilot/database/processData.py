# Standard library imports
from datetime import datetime
# Local imports
import wagerpilot.tools.apiUtils as util
import wagerpilot.tools.dbUtils as db
import wagerpilot.database.dataSupport as ds

def activeSports(writeToDb: bool = False) -> list:
    """
    :param: writeToDb (y/n to write to database)
    :return: All active sports excluding outrights
    :usage: Processes raw sports data
    """
    activeSports = []
    for item in util.sportsAPI():
        if item['active'] and not item['has_outrights']:
            data = {'key': item['key'],
                    'group': item['group'],
                    'title': item['title'],
                    'description': item['description']}
            activeSports.append(data)
    if writeToDb:
        db.insertMany('WagerSports', 'activeSports', activeSports)
    return activeSports
    
def activeEvents(writeToDb: bool = False) -> list:
    """
    :param: writeToDb (y/n to write to database)
    :return: All active events, competeting teams, and bookmaker odds
    :usage: Processes raw event data
    """
    activeEvents = []
    sports = ds.retrieveSports()
    for sport in sports:
        for event in util.eventsAPI(sport):
            if len(event['bookmakers']) == 0:
                continue
            dt = datetime.fromisoformat(event['commence_time'])
            homeTeam, awayTeam = event['home_team'], event['away_team']
            parsedOdds = ds.parseOdds(event, homeTeam, awayTeam)
            data = {'id': event['id'],
                    'sport_key': event['sport_key'],
                    'commence_date': str(dt.date()),
                    'commence_time': str(dt.time()),
                    'home_team': homeTeam,
                    'away_team': awayTeam,
                    'home_odds': parsedOdds[0],
                    'away_odds': parsedOdds[1]}
            if len(parsedOdds) == 3:
                data['draw_odds'] = parsedOdds[2]
            activeEvents.append(data)
    if writeToDb:
        db.insertMany('WagerSports', 'activeEvents', activeEvents)
    return activeEvents

def bestOdds(writeToDb: bool = False) -> list:
    """
    :param: writeToDb (y/n to write to database)
    :return: All active events, competing teams, best bookmakers odds
    :usage: Processes raw event data
    """
    bestOdds = []
    collection = db.getCollection('WagerSports', 'activeEvents')
    for event in collection.find({}):
        bestHome = ds.findBest(event['home_odds'])
        bestAway = ds.findBest(event['away_odds'])
        data = {'id': event['id'],
                'sport_key': event['sport_key'],
                'commence_date': event['commence_date'],
                'commence_time': event['commence_time'],
                'home_team': event['home_team'],
                'away_team': event['away_team'],
                'home_odds': bestHome,
                'away_odds': bestAway,}
        if 'draw_odds' in event:
            bestDraw = ds.findBest(event['draw_odds'])
            data['draw_odds'] = bestDraw
        bestOdds.append(data)
    if writeToDb:
        db.insertMany('WagerSports', 'bestOdds', bestOdds)
    return bestOdds

def arbitrageOdds(writeToDb: bool = False):
    arbitrageOdds = []
    collection = db.getCollection('WagerSports', 'bestOdds')
    for event in collection.find({}):
        data = {'id': event['id'],
                'sport_key': event['sport_key'],
                'commence_date': event['commence_date'],
                'commence_time': event['commence_time'],
                'home_team': event['home_team'],
                'away_team': event['away_team'],}
        regions = list(event['home_odds'])
        regions.extend(x for x in list(event['away_odds']) if x not in regions)
        for region in regions:
            parsedOdds = ds.parseArbitrage(event, region)
            data[region] = parsedOdds
        if data['best']['implied_probability'] < 1:
            arbitrageOdds.append(data)
    if writeToDb and len(arbitrageOdds) > 0:
        db.insertMany('WagerSports', 'arbitrageOdds', arbitrageOdds)
    return arbitrageOdds