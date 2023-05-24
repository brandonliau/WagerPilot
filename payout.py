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

def calculateArbitrageStake(eventID: str, stake: float, bias: str = 'none') -> dict:
    """
    :param: Event to bet on and total amount to bet with
    :return: Amount to bet on each team of an event
    """
    output = util.readToDict('output.json')
    odds = data.getOdds(output, eventID)
    homeTeam, awayTeam = odds['homeTeam'], odds['awayTeam']
    homeTeamOdds, awayTeamOdds = odds['homeTeamOdds'], odds['awayTeamOdds']
    total = homeTeamOdds + awayTeamOdds
    if bias == 'none':
        toWagerOnHome = (awayTeamOdds/total) * stake
        toWagerOnAway = (homeTeamOdds/total) * stake
        return {homeTeam: round(toWagerOnHome, 2), awayTeam: round(toWagerOnAway, 2)}
    elif bias == 'home_team' or bias == homeTeam:
        toWagerOnHome = stake/homeTeamOdds
        toWagerOnAway = stake - toWagerOnHome
        return {homeTeam: round(toWagerOnHome, 2), awayTeam: round(toWagerOnAway, 2)}
    elif bias == 'away_team' or bias == awayTeam:
        toWagerOnAway = stake/awayTeamOdds
        toWagerOnHome = stake - toWagerOnAway
        return {homeTeam: round(toWagerOnHome, 2), awayTeam: round(toWagerOnAway, 2)}
