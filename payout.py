import arbitrage as arb
import getData as data
import utils as util
import odds as odd

def calculatePayout(stake: float, odds: int|float|str) -> float:
    """
    :param: Amount to bet and odds (any format)
    :return: Payout
    """
    odds = odd.convertToDecimal(odds)
    return round((odds * stake), 2)

def calculateProfit(stake: float, odds: int|float|str) -> float:
    """
    :param: Amount to bet and odds (any format)
    :return: Profit (payout - stake)
    """
    payout = calculatePayout(stake, odds)
    return round((payout - stake), 2)

def calculateArbitragePayout(eventID: str, stake: float, bias: str = 'none', filePath: str = None):
    stake = arb.calculateArbitrageStake(eventID, stake, bias, filePath)
    fileData = util.readToDict(filePath)
    try:
        odds = data.getOdds(fileData, eventID)
        homeTeam, awayTeam, draw = odds['homeTeam'], odds['awayTeam'], odds['draw']
        homeOdds, awayOdds, drawOdds = odds['homeOdds'], odds['awayOdds'], odds['drawOdds']
    except:
        print('Input file is not formatted correctly!')
        exit()
    if draw == True:
        drawStake = stake['Draw']
        drawPayout = calculatePayout(drawStake, drawOdds)
    homeStake, awayStake = stake[homeTeam], stake[awayTeam]
    homePayout = calculatePayout(homeStake, homeOdds)
    awayPayout = calculatePayout(awayStake, awayOdds)
    if draw == False:
        return {homeTeam: homePayout, awayTeam: awayPayout}
    elif draw == True:
        return {homeTeam: homePayout, awayTeam: awayPayout, 'Draw': drawPayout}

def calculateArbitrageProfit(eventID: str, stake: float, bias: str = 'none', filePath: str = None):
    payout = calculateArbitragePayout(eventID, stake, bias, filePath)
    fileData = util.readToDict(filePath)
    try:
        odds = data.getOdds(fileData, eventID)
        homeTeam, awayTeam, draw = odds['homeTeam'], odds['awayTeam'], odds['draw']
    except:
        print('Input file is not formatted correctly!')
        exit()
    if draw == True:
        drawProfit = round((payout['Draw'] - stake), 2)
    homeProfit = round((payout[homeTeam] - stake), 2)
    awayProfit = round((payout[awayTeam] - stake), 2)
    if draw == False:
        return {homeTeam: homeProfit, awayTeam: awayProfit}
    elif draw == True:
        return {homeTeam: homeProfit, awayTeam: awayProfit, 'Draw': drawProfit}
