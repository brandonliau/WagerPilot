import utils as util

def getActiveSports() -> list:
    """
    :param: None
    :return: All active sports excluding those with outrights
    :usage: Processes raw sports data
    """
    activeSports = []
    for sport in util.sportsAPI():
        if sport['active'] == True and sport['has_outrights'] == False: 
            activeSports.append(sport['key'])
    return activeSports

def getActiveEvents() -> dict:
    """
    :param: None
    :return: All active events, competeting teams, and draw possiblility
    :usage: Processes raw event data
    """
    activeEvents = {}
    for sport in getActiveSports():
        for event in util.eventsAPI(sport):
            draw = False
            if len(event['bookmakers']) > 0:
                for item in event['bookmakers']: 
                    if len(item['markets'][0]['outcomes']) == 3:
                        draw = True
            activeEvents[event['id']] = {'homeTeam': event['home_team'], 'awayTeam': event['away_team'], 'draw': draw}
    return activeEvents

def getAllOdds(writeToFile: bool = True, fileName: str = None):
    """
    :param: writeToFile (y/n to write output to json), fileName (name of output file)
    :return: All active events, competing teams, odds, and bookmakers
    :usage: Processes raw event data
    """
    allOdds = {}
    for sport in getActiveSports():
        for event in util.eventsAPI(sport):
            outerTempDict = {}
            home_team, away_team, draw = event['home_team'], event['away_team'], False
            for bookie in event['bookmakers']:
                innerTempDict = {}
                for item in bookie['markets'][0]['outcomes']:
                    if item['name'] == home_team:
                        innerTempDict['homeTeam'] = item['price']
                    if item['name'] == away_team:
                        innerTempDict['awayTeam'] = item['price']
                    if item['name'] == 'Draw':
                        innerTempDict['draw'] = item['price']
                        draw = True
                outerTempDict[bookie['key']] = innerTempDict
            if len(outerTempDict) > 0:
                allOdds[event['id']] = {'homeTeam': home_team, 'awayTeam': away_team, 'draw': draw, 'odds': outerTempDict}
    if writeToFile == True:
        util.writeToJson(allOdds, fileName)
    return allOdds

def getBestOdds(writeToFile: bool = True, fileName: str = None):
    """
    :param: writeToFile (y/n to write output to json), fileName (name of output file)
    :return: All active events, competing teams, best odds, and best bookmakers
    :usage: Processes raw event data
    """
    bestOdds = {}
    for sport in getActiveSports():
        for event in util.eventsAPI(sport):
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

def getEventOdds(data: dict, eventID: str) -> dict:
    """
    :param: data (eg. output from getAllOdds), eventID (event to search)
    :return: Event odds and bookmakers for a given event
    :usage: Obtains odds data for a specific event
    """
    return data[eventID]