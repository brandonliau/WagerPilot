# Standard library imports
from datetime import datetime
# Third party imports
from pymongo import MongoClient
# Local imports
import wagerpilot.config as con
import wagerpilot.tools.apiUtils as util
import wagerpilot.tools.dbUtils as db
import wagerpilot.database.dataSupport as ds
import wagerpilot.support.bookmakers as bookie

def activeSports(writeToDb: bool = False) -> list:
    """
    :param: writeToDb (y/n to write to database)
    :return: All active sports excluding those with outrights
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
    :return: All active events, competeting teams, and draw possiblility
    :usage: Processes raw event data
    """
    activeEvents = []
    sports = db.retrieveSports('WagerSports', 'activeSports', {'key':1, '_id':0})
    for sport in sports:
        for event in util.eventsAPI(sport):
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

def bestOdds(writeToDb: bool = False) -> dict:
    """
    :param: writeToDb (y/n to write to database)
    :return: All active events, competing teams, best odds, and best bookmakers
    :usage: Processes raw event data
    """
    bestOdds = []
    client = MongoClient(con.mongoConnectionString)
    collection = client['WagerSports']['activeEvents']
    for event in collection.find({}):
        bestHome = ds.findBestOdds(event['home_odds'])
        bestAway = ds.findBestOdds(event['away_odds'])
        data = {'id': event['id'],
                'sport_key': event['sport_key'],
                'commence_date': event['commence_date'],
                'commence_time': event['commence_time'],
                'home_team': event['home_team'],
                'away_team': event['away_team'],
                'home_odds': bestHome,
                'away_odds': bestAway,}
        if 'draw_odds' in event:
            bestDraw = ds.findBestOdds(event['draw_odds'])
            data['draw_odds'] = bestDraw
        bestOdds.append(data)
    if writeToDb:
        db.insertMany('WagerSports', 'bestOdds', bestOdds)
    return bestOdds
