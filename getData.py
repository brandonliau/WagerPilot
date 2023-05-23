import config as con
from pprint import pprint
import requests

def sportsAPI():
    oddsAPIKey = next(con.oddsAPIKeyCycle)
    url = f'https://api.the-odds-api.com/v4/sports/?apiKey={oddsAPIKey}'
    response = requests.request("GET", url)
    return(response.json())

def eventsAPI(sport):
    oddsAPIKey = next(con.oddsAPIKeyCycle)
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={oddsAPIKey}&regions=us,us2,uk,au,eu&markets=h2h&oddsFormat=decimal'
    response = requests.request("GET", url)
    return(response.json())

def getActiveSports():
    sportsList = []
    sports = sportsAPI()
    for item in sports:
        if item['active'] == True and item['has_outrights'] == False: 
            sportsList.append(item['key'])
    return sportsList

def getOdds(input, eventID):
    odds = {}
    odds['homeTeam'] = input[eventID]['homeTeam']
    odds['awayTeam'] = input[eventID]['awayTeam']
    odds['homeTeamOdds'] = input[eventID]['homeTeamOdds']
    odds['awayTeamOdds'] = input[eventID]['awayTeamOdds']
    return odds

def getKeyQuotas():
    keyUsage = {}
    for apiKey in con.oddsAPIKeys:
        url = f'https://api.the-odds-api.com/v4/sports/?apiKey={apiKey}'
        response = requests.request("GET", url)
        requestsRemaining = response.headers['X-Requests-Remaining']
        requestsUsed = response.headers['X-Requests-Used']
        keyUsage[apiKey] = {'Remaining': requestsRemaining, 'Used': requestsUsed}
    return(keyUsage)

# pprint(getKeyQuotas())