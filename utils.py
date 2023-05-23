import getData as data
from pprint import pprint
import json

def writeToJson(input):
    json_object = json.dumps(input, indent=4)
    with open("output.json", "w") as file:
        file.write(json_object)

def writeToDict(input):
    with open(input) as file:
        output = json.load(file)
    return output

def findArbitrage():
    activeSports = data.getActiveSports()
    aribtrageOpportunity = {}
    for sport in activeSports:
        events = data.eventsAPI(sport)
        for event in events:
            tempDict = {}
            home_team = event['home_team']
            away_team = event['away_team']
            tempDict['homeTeam'] = home_team
            tempDict['awayTeam'] = away_team
            for bookie in event['bookmakers']:
                if len(tempDict) == 2:
                    tempDict['homeBookie'] = [bookie['key']]
                    tempDict['awayBookie'] = [bookie['key']]
                    for item in bookie['markets'][0]['outcomes']:
                        if item['name'] == home_team:
                            tempDict['homeTeamOdds'] = item['price']
                        if item['name'] == away_team:
                            tempDict['awayTeamOdds'] = item['price']
                else:
                    for item in bookie['markets'][0]['outcomes']:
                        if item['name'] == home_team and item['price'] > tempDict['homeTeamOdds']:
                            tempDict['homeTeamOdds'] = item['price']
                            tempDict['homeBookie'] = [bookie['key']]
                        elif item['name'] == home_team and item['price'] == tempDict['homeTeamOdds']:
                            tempDict['homeBookie'].append(bookie['key'])
                        if item['name'] == away_team and item['price'] > tempDict['awayTeamOdds']:
                            tempDict['awayTeamOdds'] = item['price']
                            tempDict['awayBookie'] = [bookie['key']]
                        elif item['name'] == away_team and item['price'] == tempDict['awayTeamOdds']:
                            tempDict['awayBookie'].append(bookie['key'])
                ev = 1/tempDict['homeTeamOdds'] + 1/tempDict['awayTeamOdds']
                if ev < 1:
                    tempDict['EV'] = ev
                    aribtrageOpportunity[event['id']] = tempDict
    return aribtrageOpportunity

# arbitrage = findArbitrage()
# writeToJson(arbitrage)
# pprint(findArbitrage())