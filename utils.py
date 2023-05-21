import getData as data
import json

def isArbitrage(homeOdds, awayOdds):
    if (1/homeOdds + 1/awayOdds) < 1.0:
        return True
    else:
        return False

def findArbitrage():
    activeSports = data.getActiveSports()
    possibleArbitrage, aribtrageOpportunity = {}, {}
    for sport in activeSports:
        events = data.eventsAPI(sport)
        for event in events:
            tempDict = {}
            home_team = event['home_team']
            away_team = event['away_team']
            for bookie in event['bookmakers']:
                if len(tempDict) == 0:
                    tempDict['homeBookie'] = [bookie['key']]
                    tempDict['awayBookie'] = [bookie['key']]
                    for item in bookie['markets'][0]['outcomes']:
                        if item['name'] == home_team:
                            tempDict['homeTeam'] = item['price']
                        if item['name'] == away_team:
                            tempDict['awayTeam'] = item['price']
                else:
                    for item in bookie['markets'][0]['outcomes']:
                        if item['name'] == home_team and item['price'] > tempDict['homeTeam']:
                            tempDict['homeTeam'] = item['price']
                            tempDict['homeBookie'] = [bookie['key']]
                        elif item['name'] == home_team and item['price'] == tempDict['homeTeam']:
                            tempDict['homeBookie'].append(bookie['key'])
                        if item['name'] == away_team and item['price'] > tempDict['awayTeam']:
                            tempDict['awayTeam'] = item['price']
                            tempDict['awayBookie'] = [bookie['key']]
                        elif item['name'] == away_team and item['price'] == tempDict['awayTeam']:
                            tempDict['awayBookie'].append(bookie['key'])
                ev = 1/tempDict['homeTeam'] + 1/tempDict['awayTeam']
                if ev < 1:
                    tempDict['EV'] = ev
                    possibleArbitrage[event['id']] = tempDict
    return possibleArbitrage

# with open('output.json', 'r') as file:
#   events = json.load(file)
# print(events)
# print(findArbitrage(events))
print(findArbitrage())