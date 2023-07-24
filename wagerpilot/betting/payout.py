# Local imports
import wagerpilot.betting.odds as odd
import wagerpilot.betting.probability as prob

def payout(stake: float, odds: int|float|str) -> float:
    """
    :param: stake, odds (any format)
    :return: Payout
    :usage: Calculate payout of a bet
    """
    return odd.toDecimal(odds) * stake

def profit(stake: float, odds: int|float|str) -> float:
    """
    :param: stake, odds (any format)
    :return: Profit
    :usage: Calculate profit of a bet
    """
    return payout(stake, odds) - stake

def expectedValue(toBet: str, homeOdds: float, awayOdds: float, drawOdds: float = None) -> float:
    """
    :param: toBet (team to bet on), homeOdds, awayOdds, drawOdds (any format)
    :return: Expected value for given bet
    :usage: Calculate the expected value for a bet given the odds of an event
    """
    trueProb = prob.trueProability(homeOdds, awayOdds, drawOdds)
    homeOdds, awayOdds, drawOdds = odd.toDecimal(homeOdds), odd.toDecimal(awayOdds), odd.toDecimal(drawOdds)
    if toBet == 'home':
        winProb = trueProb['homeTrue']
        winProfit = profit(1, homeOdds)
    elif toBet == 'away':
        winProb = trueProb['awayTrue']
        winProfit = profit(1, awayOdds)
    elif drawOdds != None and toBet == 'draw':
        winProb = trueProb['drawTrue']
        winProfit = profit(1, drawOdds)
    loseProb = 1 - winProb
    return (winProfit * winProb) - (1 * loseProb)

# To be refactored
# def arbitragePayout(eventID: str, stake: float, bias: str = 'none', fileName: str = None) -> dict:
#     """
#     :param: eventID, stake, bias (maximized profit for biased team), fileName (name of input file)
#     :return: Payout for each event outcome
#     :usage: Calculate payout for each event outcome in an arbitrage bet
#     """
#     stake = arb.arbitrageStake(eventID, stake, bias, fileName)
#     if fileName == None:
#         fileData = get.bestOdds()
#     else:
#         fileData = util.readFromJson(fileName)
#     try:
#         odds = get.eventOdds(fileData, eventID)
#         homeTeam, awayTeam, draw = odds['homeTeam'], odds['awayTeam'], odds['draw']
#         homeOdds, awayOdds, drawOdds = odds['homeOdds'], odds['awayOdds'], odds['drawOdds']
#     except:
#         print('Input file is not formatted correctly!')
#         exit()
#     if draw == True:
#         drawStake = stake['Draw']
#         drawPayout = payout(drawStake, drawOdds)
#     homeStake, awayStake = stake[homeTeam], stake[awayTeam]
#     homePayout = payout(homeStake, homeOdds)
#     awayPayout = payout(awayStake, awayOdds)
#     if draw == False:
#         return {homeTeam: homePayout, awayTeam: awayPayout}
#     elif draw == True:
#         return {homeTeam: homePayout, awayTeam: awayPayout, 'Draw': drawPayout}

# def arbitrageProfit(eventID: str, stake: float, bias: str = 'none', fileName: str = None) -> dict:
#     """
#     :param: eventID, stake, bias (maximized profit for biased team), fileName (name of input file)
#     :return: Profit for each event outcome
#     :usage: Calculate profit for each event outcome in an arbitrage bet
#     """
#     payout = arbitragePayout(eventID, stake, bias, fileName)
#     fileData = util.readFromJson(fileName)
#     try:
#         odds = get.eventOdds(fileData, eventID)
#         homeTeam, awayTeam, draw = odds['homeTeam'], odds['awayTeam'], odds['draw']
#     except:
#         print('Input file is not formatted correctly!')
#         exit()
#     if draw == True:
#         drawProfit = round((payout['Draw'] - stake), 2)
#     homeProfit = round((payout[homeTeam] - stake), 2)
#     awayProfit = round((payout[awayTeam] - stake), 2)
#     if draw == False:
#         return {homeTeam: homeProfit, awayTeam: awayProfit}
#     elif draw == True:
#         return {homeTeam: homeProfit, awayTeam: awayProfit, 'Draw': drawProfit}

