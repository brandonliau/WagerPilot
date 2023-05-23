import getData as data
import utils as util
import odds as odd

def calculatePayout(stake: float, odds: int|float|str) -> float:
    """
    :param: Amount to bet and odds (given in any format)
    :return: Payout
    """
    odds = odd.convertToDecimal(odds)
    return (odds * stake)

def calculateProfit(stake: float, odds: int|float|str) -> float:
    """
    :param: Amount to bet and odds (given in any format)
    :return: Profit (payout - stake)
    """
    payout = calculatePayout(stake, odds)
    return (payout - stake)

def calculateArbitrageStake(eventID, stake):
    """
    :param: Event to bet on and total amount to bet with
    :return: Amount to bet on each team of an event
    """
    output = util.writeToDict('output.json')
    odds = data.getOdds(output, eventID)
    homeTeam, awayTeam = odds['homeTeam'], odds['awayTeam']
    homeTeamOdds, awayTeamOdds = odds['homeTeamOdds'], odds['awayTeamOdds']
    total = homeTeamOdds + awayTeamOdds
    toWagerOnHome = (awayTeamOdds/total) * stake
    toWagerOnAway = (homeTeamOdds/total) * stake
    return {homeTeam: round(toWagerOnHome, 2), awayTeam: round(toWagerOnAway, 2)}

