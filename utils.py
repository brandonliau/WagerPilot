import getData as data
import json

def writeToJson(toWrite: dict, fileName: json, overWrite: bool = True) -> None:
    """
    :param: Data to write (eg. getActiveSports), file to write to (eg. 'output.json'), whether to over write the file
    :return: None
    """
    json_object = json.dumps(toWrite, indent=4)
    if overWrite == True:
        with open(fileName, 'w') as file:
            file.write(json_object)
    else:
        with open(fileName, 'a') as file:
            file.write(json_object)

def readToDict(toRead: json) -> dict:
    """
    :param: Data to read (eg. 'output.json')
    :return: Data from json file
    """
    with open(toRead, 'r') as file:
        output = json.load(file)
    return output

def findArbitrage() -> dict:
    """
    :param: None
    :return: All arbitrage opportunities
    """
    aribtrageOpportunities = {}
    for sport in data.getActiveSports():
        for event in data.eventsAPI(sport):
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
                            tempDict['homeTeamOdds'] = item['price']
                        if item['name'] == away_team:
                            tempDict['awayTeamOdds'] = item['price']
                        if item['name'] == 'Draw':
                            tempDict['drawBookie'] = [bookie['key']]
                            tempDict['drawOdds'] = item['price']
                            tempDict['draw'] = True
                        else:
                            tempDict['drawBookie'] = None
                            tempDict['drawOdds'] = None
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
                        if item['name'] == 'Draw' and (tempDict['drawOdds'] is None or item['price'] > tempDict['drawOdds']):
                            tempDict['drawOdds'] = item['price']
                            tempDict['drawBookie'] = [bookie['key']]
                            tempDict['draw'] = True
                        elif item['name'] == 'Draw' and item['price'] == tempDict['drawOdds']:
                            tempDict['drawBookie'].append(bookie['key'])
                if tempDict['draw'] == True:
                    ev = (1/tempDict['homeTeamOdds']) + (1/tempDict['awayTeamOdds'] + 1/tempDict['drawOdds'])
                else: 
                    ev = (1/tempDict['homeTeamOdds']) + (1/tempDict['awayTeamOdds'])
                if ev < 1:
                    tempDict['EV'] = ev
                    aribtrageOpportunities[event['id']] = tempDict
    return aribtrageOpportunities
