import getData as data
import utils as util
import time

def findArbitrage(writeToFile: bool = True, fileName: str = None) -> dict:
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
                if tempDict['draw'] == True:
                    impliedProbability = (1/tempDict['homeOdds']) + (1/tempDict['awayOdds'] + 1/tempDict['drawOdds'])
                else: 
                    impliedProbability = (1/tempDict['homeOdds']) + (1/tempDict['awayOdds'])
                if impliedProbability < 1:
                    tempDict['impliedProbability'] = impliedProbability
                    aribtrageOpportunities[event['id']] = tempDict
    if writeToFile == True and fileName == None:
        localTime = time.strftime("%H:%M:%S", time.localtime())
        util.writeToJson(aribtrageOpportunities, fileName = f'{localTime}.json')
    elif writeToFile == True:
        util.writeToJson(aribtrageOpportunities, fileName = f'{fileName}.json')
    return aribtrageOpportunities

def calculateArbitrageStake(eventID: str, stake: float, bias: str = 'none', filePath: str = None) -> dict:
    """
    :param: Event to bet on and total amount to bet with
    :return: Amount to bet on each team of an event
    """
    fileData = util.readToDict(filePath)
    try:
        odds = data.getOdds(fileData, eventID)
        homeTeam, awayTeam, draw = odds['homeTeam'], odds['awayTeam'], odds['draw']
        homeOdds, awayOdds, drawOdds = odds['homeOdds'], odds['awayOdds'], odds['drawOdds']
        homePercentage, awayPercentage, drawPercentage = 1/(homeOdds), 1/(awayOdds), util.div(1, drawOdds)
    except:
        print('Input file is not formatted correctly!')
        exit()
    if bias == 'none':
        totalPercentage = homePercentage + awayPercentage + drawPercentage
        toWagerOnHome  = (homePercentage / totalPercentage) * stake
        toWagerOnAway  = (awayPercentage / totalPercentage) * stake
        toWagerOnDraw  = (drawPercentage / totalPercentage) * stake
    elif bias == 'home_team' or bias == homeTeam:
        toWagerOnAway = stake / awayOdds
        toWagerOnDraw = util.div(stake, drawOdds)
        toWagerOnHome = stake - toWagerOnAway - toWagerOnDraw
    elif bias == 'away_team' or bias == awayTeam:
        toWagerOnHome = stake / homeOdds
        toWagerOnDraw = util.div(stake, drawOdds)
        toWagerOnAway = stake - toWagerOnHome - toWagerOnDraw
    elif bias == 'draw':
        toWagerOnHome = stake / homeOdds
        toWagerOnAway = stake / awayOdds
        toWagerOnDraw = stake - toWagerOnHome - toWagerOnAway
    if draw == False:
        return {homeTeam: round(toWagerOnHome, 2), awayTeam: round(toWagerOnAway, 2)}
    elif draw == True:
        return {homeTeam: round(toWagerOnHome, 2), awayTeam: round(toWagerOnAway, 2), 'Draw': round(toWagerOnDraw, 2)}