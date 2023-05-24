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
