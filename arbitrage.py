import utils as util
import getData as get

def findArbitrage(readFileName: str = None, writeToFile: bool = True, writefileName: str = None) -> dict:
    """
    :param: readFileName (name of input file), writeToFile (y/n to write output to json), writefileName (name of output file)
    :return: All arbitrage opportunities
    :usage: Find all arbitrage opportunities
    """
    aribtrageOpportunities = {}
    if readFileName == None:
        bestOdds = get.bestOdds()
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

def arbitrageStake(eventID: str, stake: float, bias: str = None, fileName: str = None) -> dict:
    """
    :param: eventID, stake, bias (maximizes payout for biased team), fileName (name of input file)
    :return: Amount to bet on each team
    :usage: Calculate amount to bet on each team to achieve an arbitrage bet
    """
    if fileName == None:
        fileData = get.bestOdds()
    else:
        fileData = util.readFromJson(fileName)
    try:
        odds = get.eventOdds(fileData, eventID)
        homeTeam, awayTeam = odds['homeTeam'], odds['awayTeam']
        homeOdds, awayOdds, drawOdds = odds['homeOdds'], odds['awayOdds'], odds['drawOdds']
        homePercentage, awayPercentage, drawPercentage = 1/(homeOdds), 1/(awayOdds), util.div(1, drawOdds)
    except:
        print('Input file is not formatted correctly!')
        exit()
    if bias == None:
        total = homePercentage + awayPercentage + drawPercentage
        homeWager  = (homePercentage / total) * stake
        awayWager  = (awayPercentage / total) * stake
        drawWager  = (drawPercentage / total) * stake
    elif bias == 'home' or bias == homeTeam:
        awayWager = stake / awayOdds
        drawWager = util.div(stake, drawOdds)
        homeWager = stake - awayWager - drawWager
    elif bias == 'away' or bias == awayTeam:
        homeWager = stake / homeOdds
        drawWager = util.div(stake, drawOdds)
        awayWager = stake - homeWager - drawWager
    elif bias == 'draw':
        homeWager = stake / homeOdds
        awayWager = stake / awayOdds
        drawWager = stake - homeWager - awayWager
    return {homeTeam: round(homeWager, 2), awayTeam: round(awayWager, 2), 'Draw': round(drawWager, 2)}