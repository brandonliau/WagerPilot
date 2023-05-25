import getData as data
import utils as util

def findArbitrage(readFileName: str = None, writeToFile: bool = True, writefileName: str = None) -> dict:
    """
    :param: readFileName (name of input file), writeToFile (y/n to write output to json), writefileName (name of output file)
    :return: All arbitrage opportunities
    :usage: Fid all arbitrage opportunities
    """
    aribtrageOpportunities = {}
    if readFileName == None:
        bestOdds = data.findBestOdds()
    else:
        bestOdds = util.readFromJson(readFileName)
    for event in bestOdds:
        impliedProbability = 1/bestOdds[event]['homeOdds'] + 1/bestOdds[event]['awayOdds'] + util.div(1, bestOdds[event]['drawOdds'])
        if impliedProbability < 1:
            bestOddsCopy = bestOdds[event].copy()
            bestOddsCopy['impliedProbability'] = impliedProbability
            aribtrageOpportunities[event] = bestOddsCopy
    if writeToFile == True:
        util.writeToJson(aribtrageOpportunities, writefileName)
    return aribtrageOpportunities

def calculateArbitrageStake(eventID: str, stake: float, bias: str = None, fileName: str = None) -> dict:
    """
    :param: eventID, stake, bias (maximizes payout for biased team), fileName (name of input file)
    :return: Amount to bet on each team
    :usage: Calculate amount to bet on each team to achieve an arbitrage bet
    """
    if fileName == None:
        fileData = data.findBestOdds()
    else:
        fileData = util.readFromJson(fileName)
    try:
        odds = data.getEventOdds(fileData, eventID)
        homeTeam, awayTeam, draw = odds['homeTeam'], odds['awayTeam'], odds['draw']
        homeOdds, awayOdds, drawOdds = odds['homeOdds'], odds['awayOdds'], odds['drawOdds']
        homePercentage, awayPercentage, drawPercentage = 1/(homeOdds), 1/(awayOdds), util.div(1, drawOdds)
    except:
        print('Input file is not formatted correctly!')
        exit()
    if bias == None:
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