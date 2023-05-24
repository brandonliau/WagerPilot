import config as con
import requests

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

def getArbOdds(arbOpportunities: dict, eventID: str) -> dict:
    """
    :param: Arbitrage opportunities (eg. obtained from findArbitrage)
    :return: Odds for the arbitrage opportunity
    """
    getArbOdds = {}
    getArbOdds['homeTeam'] = arbOpportunities[eventID]['homeTeam']
    getArbOdds['awayTeam'] = arbOpportunities[eventID]['awayTeam']
    getArbOdds['homeTeamOdds'] = arbOpportunities[eventID]['homeTeamOdds']
    getArbOdds['awayTeamOdds'] = arbOpportunities[eventID]['awayTeamOdds']
    # getArbOdds['draw'] = 'draw'
    # getArbOdds['drawOdds'] = arbOpportunities[eventID]['awayTeamOdds']
    return getArbOdds

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
