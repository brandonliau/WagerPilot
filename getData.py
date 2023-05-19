import config as con
import requests

def sportsAPI():
    oddsAPIKey = next(con.oddsAPIKeys)
    url = f'https://api.the-odds-api.com/v4/sports/?apiKey={oddsAPIKey}'
    response = requests.request("GET", url)
    return(response.json())

def eventsAPI(sport):
    oddsAPIKey = next(con.oddsAPIKeys)
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

# print(getActiveSports())
# print(eventsAPI())
# sportList = getActiveSports()
# print(getActiveEvents(sportList))
