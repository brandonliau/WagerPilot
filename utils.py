import config as con
import requests
import json
import time

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
    :param: sportKey (eg. americanfootball_nfl)
    :return: All events and other relevant data for a given sport
    :usage: Provides raw event data
    """
    oddsAPIKey = next(con.oddsAPIKeyCycle)
    url = f'https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?apiKey={oddsAPIKey}&regions=us,us2,uk,au,eu&markets=h2h&oddsFormat=decimal'
    response = requests.request("GET", url)
    return(response.json())

def keyUsage(key: str = 'all') -> dict:
    """
    :param: Specific API key (optional)
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

def div(x: float, y: float):
    """
    :param: x, y
    :return: Quotient of x and y
    :usage: Allow division of two numbers even if denominator is None
    """
    try:
        return x/y
    except TypeError:
        return 0

def writeToJson(data: dict, fileName: str = None) -> None:
    """
    :param: data (eg. provided by getAllOdds), fileName (name of output file)
    :return: None
    :usage: Write dictionary data to json file
    """
    json_object = json.dumps(data, indent=4)
    if fileName == None:
        localTime = time.strftime("%H:%M:%S", time.localtime())
        with open(f'{localTime}.json', 'w') as file:
            file.write(json_object)
    else:
        with open(fileName, 'w') as file:
            file.write(json_object)

def readFromJson(fileName: str) -> dict:
    """
    :param: fileName (name of input file)
    :return: Data from json file
    :usage: Read json file and return it as a dictionary
    """
    try:
        with open(fileName, 'r') as file:
            output = json.load(file)
        return output
    except FileNotFoundError:
        print('Input file does not exist!')
        exit()