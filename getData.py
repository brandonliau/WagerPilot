import config as con
import utils as util
import requests
import time

def sportsAPI() -> dict:
    """
    :param: None
    :return: All sports
    """
    oddsAPIKey = next(con.oddsAPIKeyCycle)
    url = f'https://api.the-odds-api.com/v4/sports/?apiKey={oddsAPIKey}'
    response = requests.request("GET", url)
    return(response.json())

def eventsAPI(sportKey: str) -> dict:
    """
    :param: sport_key (eg. americanfootball_nfl)
    :return: All events for the given sport
    """
    oddsAPIKey = next(con.oddsAPIKeyCycle)
    url = f'https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?apiKey={oddsAPIKey}&regions=us,us2,uk,au,eu&markets=h2h&oddsFormat=decimal'
    response = requests.request("GET", url)
    return(response.json())

def getActiveSports() -> list:
    """
    :param: None
    :return: All active sports
    """
    activeSports = []
    for sport in sportsAPI():
        if sport['active'] == True and sport['has_outrights'] == False: 
            activeSports.append(sport['key'])
    return activeSports

def getActiveEvents() -> dict:
    """
    :param: None
    :return: All active events and the teams competing
    """
    activeEvents = {}
    for sport in getActiveSports():
        for event in eventsAPI(sport):
            draw = False
            if len(event['bookmakers']) > 0:
                for item in event['bookmakers']: 
                    if len(item['markets'][0]['outcomes']) == 3:
                        draw = True
            activeEvents[event['id']] = {'homeTeam': event['home_team'], 'awayTeam': event['away_team'], 'draw': draw}
    return activeEvents

def getOdds(bestOdds: dict, eventID: str) -> dict:
    """
    :param: Best odds (eg. obtained from bestOdds)
    :return: Odds for the given event
    """
    odds = {}
    odds['homeTeam'] = bestOdds[eventID]['homeTeam']
    odds['awayTeam'] = bestOdds[eventID]['awayTeam']
    odds['homeOdds'] = bestOdds[eventID]['homeOdds']
    odds['awayOdds'] = bestOdds[eventID]['awayOdds']
    odds['draw'] = bestOdds[eventID]['draw']
    odds['drawOdds'] = bestOdds[eventID]['drawOdds']
    return odds

def getBestOdds(writeToFile: bool = True, fileName: str = None):
    bestOdds = {}
    for sport in getActiveSports():
        for event in eventsAPI(sport):
            tempDict = {}
            home_team = event['home_team']
            away_team = event['away_team']
            tempDict['homeTeam'] = home_team
            tempDict['awayTeam'] = away_team
            tempDict['draw'] = False
            for bookie in event['bookmakers']:
                if len(tempDict) == 3:
                    tempDict['homeBookie'] = [bookie['key']]
                    tempDict['awayBookie'] = [bookie['key']]
                    tempDict['drawBookie'] = None
                    for item in bookie['markets'][0]['outcomes']:
                        if item['name'] == home_team:
                            tempDict['homeOdds'] = item['price']
                        if item['name'] == away_team:
                            tempDict['awayOdds'] = item['price']
                        if item['name'] == 'Draw':
                            tempDict['drawBookie'] = [bookie['key']]
                            tempDict['drawOdds'] = item['price']
                            tempDict['draw'] = True
                        else:
                            tempDict['drawBookie'] = None
                            tempDict['drawOdds'] = None
                else:
                    for item in bookie['markets'][0]['outcomes']:
                        if item['name'] == home_team and item['price'] > tempDict['homeOdds']:
                            tempDict['homeOdds'] = item['price']
                            tempDict['homeBookie'] = [bookie['key']]
                        elif item['name'] == home_team and item['price'] == tempDict['homeOdds']:
                            tempDict['homeBookie'].append(bookie['key'])
                        if item['name'] == away_team and item['price'] > tempDict['awayOdds']:
                            tempDict['awayOdds'] = item['price']
                            tempDict['awayBookie'] = [bookie['key']]
                        elif item['name'] == away_team and item['price'] == tempDict['awayOdds']:
                            tempDict['awayBookie'].append(bookie['key'])
                        if item['name'] == 'Draw' and (tempDict['drawOdds'] is None or item['price'] > tempDict['drawOdds']):
                            tempDict['drawOdds'] = item['price']
                            tempDict['drawBookie'] = [bookie['key']]
                            tempDict['draw'] = True
                        elif item['name'] == 'Draw' and item['price'] == tempDict['drawOdds']:
                            tempDict['drawBookie'].append(bookie['key'])
                bestOdds[event['id']] = tempDict
    if writeToFile == True:
        util.writeToJson(bestOdds, fileName)
    return bestOdds
    
def getKeyUsage(key: str = 'all') -> dict:
    """
    :param: None
    :return: Reamaining requests and requests used for all API keys
    """
    keyUsage = {}
    if key == 'all':
        for apiKey in con.oddsAPIKeys:
            url = f'https://api.the-odds-api.com/v4/sports/?apiKey={apiKey}'
            response = requests.request("GET", url)
            requestsRemaining = response.headers['X-Requests-Remaining']
            requestsUsed = response.headers['X-Requests-Used']
            keyUsage[apiKey] = {'Remaining': requestsRemaining, 'Used': requestsUsed}
    else:
        url = f'https://api.the-odds-api.com/v4/sports/?apiKey={key}'
        response = requests.request("GET", url)
        requestsRemaining = response.headers['X-Requests-Remaining']
        requestsUsed = response.headers['X-Requests-Used']
        keyUsage[key] = {'Remaining': requestsRemaining, 'Used': requestsUsed}
    return(keyUsage)
