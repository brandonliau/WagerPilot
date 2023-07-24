# Third party imports
import requests
# Local imports
import wagerpilot.config as con

def sportsAPI() -> dict:
    """
    :param: None
    :return: All sports and other relevant data
    :usage: Provides raw sports data
    """
    oddsAPIKey = next(con.oddsAPIKeyCycle)
    url = f'https://api.the-odds-api.com/v4/sports/?apiKey={oddsAPIKey}'
    response = requests.request("GET", url)
    return(response.json())

def eventsAPI(sportKey: str) -> dict:
    """
    :param: sportKey (eg. americanfootball_nfl), regions (eg. us,us2)
    :return: All events and other relevant data for a given sport
    :usage: Provides raw event data
    """
    oddsAPIKey = next(con.oddsAPIKeyCycle)
    url = f'https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?apiKey={oddsAPIKey}&regions={con.regions}&markets=h2h&oddsFormat=decimal'
    response = requests.request("GET", url)
    return(response.json())

def keyUsage(key: str = 'all') -> dict:
    """
    :param: key (specific API key, optional)
    :return: Number of remaining requests and requests used for API key(s)
    :usage: Check usage of API key(s)
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
