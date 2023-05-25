import getData as data
import utils as util

def findAllOdds(writeToFile: bool = True, fileName: str = None):
    allOdds = {}
    for sport in data.getActiveSports():
        for event in data.eventsAPI(sport):
            outerTempDict = {}
            home_team, away_team = event['home_team'], event['away_team']
            for bookie in event['bookmakers']:
                innerTempDict = {}
                for item in bookie['markets'][0]['outcomes']:
                    if item['name'] == home_team:
                        innerTempDict['homeTeam'] = item['price']
                    if item['name'] == away_team:
                        innerTempDict['awayTeam'] = item['price']
                    if item['name'] == 'Draw':
                        innerTempDict['draw'] = item['price']
                outerTempDict[bookie['key']] = innerTempDict
            if len(outerTempDict) > 0:
                allOdds[event['id']] = {'homeTeam': home_team, 'awayTeam': away_team, 'odds': outerTempDict}
    if writeToFile == True:
        util.writeToJson(allOdds, fileName)
    return allOdds

def findBestOdds(writeToFile: bool = True, fileName: str = None):
    bestOdds = {}
    for sport in data.getActiveSports():
        for event in data.eventsAPI(sport):
            tempDict = {}
            home_team, away_team = event['home_team'], event['away_team']
            tempDict['homeTeam'], tempDict['awayTeam'] = home_team, away_team
            tempDict['draw'] = False
            for bookie in event['bookmakers']:
                if len(tempDict) == 3:
                    tempDict['homeBookie'] = [bookie['key']]
                    tempDict['awayBookie'] = [bookie['key']]
                    tempDict['drawBookie'] = None
                    for item in bookie['markets'][0]['outcomes']:
                        if item['name'] == home_team:
                            tempDict['homeOdds'] = item['price']
                        if item['name'] == away_team:
                            tempDict['awayOdds'] = item['price']
                        if item['name'] == 'Draw':
                            tempDict['drawBookie'] = [bookie['key']]
                            tempDict['drawOdds'] = item['price']
                            tempDict['draw'] = True
                        else:
                            tempDict['drawBookie'] = None
                            tempDict['drawOdds'] = None
                else:
                    for item in bookie['markets'][0]['outcomes']:
                        if item['name'] == home_team and item['price'] > tempDict['homeOdds']:
                            tempDict['homeOdds'] = item['price']
                            tempDict['homeBookie'] = [bookie['key']]
                        elif item['name'] == home_team and item['price'] == tempDict['homeOdds']:
                            tempDict['homeBookie'].append(bookie['key'])
                        if item['name'] == away_team and item['price'] > tempDict['awayOdds']:
                            tempDict['awayOdds'] = item['price']
                            tempDict['awayBookie'] = [bookie['key']]
                        elif item['name'] == away_team and item['price'] == tempDict['awayOdds']:
                            tempDict['awayBookie'].append(bookie['key'])
                        if item['name'] == 'Draw' and (tempDict['drawOdds'] is None or item['price'] > tempDict['drawOdds']):
                            tempDict['drawOdds'] = item['price']
                            tempDict['drawBookie'] = [bookie['key']]
                            tempDict['draw'] = True
                        elif item['name'] == 'Draw' and item['price'] == tempDict['drawOdds']:
                            tempDict['drawBookie'].append(bookie['key'])
                bestOdds[event['id']] = tempDict
    if writeToFile == True:
        util.writeToJson(bestOdds, fileName)
    return bestOdds