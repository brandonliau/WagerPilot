import config as con
import requests
import json
from pprint import pprint

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

def getActiveEvents(sportsList):
    eventDict = {}
    for sport in sportsList:
        tempList = []
        for item in eventsAPI(sport):
            tempList.append(item['id'])
        eventDict[sport] = tempList
    return eventDict

def writeToJson():
    sportsList = getActiveSports()
    for sport in sportsList:
        json_object = json.dumps(eventsAPI(sport), indent=4)
        with open("output.json", "a") as outfile:
            outfile.write(json_object)

def getKeyQuotas():
    keyUsage = {}
    for apiKey in con.oddsAPIKeys:
        url = f'https://api.the-odds-api.com/v4/sports/?apiKey={apiKey}'
        response = requests.request("GET", url)
        requestsRemaining = response.headers['X-Requests-Remaining']
        requestsUsed = response.headers['X-Requests-Used']
        keyUsage[apiKey] = {'Remaining': requestsRemaining, 'Used': requestsUsed}
    return(keyUsage)

pprint(getKeyQuotas())