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
