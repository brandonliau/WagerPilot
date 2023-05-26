from fractions import Fraction
import utils as util
import math

def convertToDecimal(odds: int|float|str) -> float:
    """
    :param: Odds (any format)
    :return: Odds in decimal format
    :usage: Convert odds to decimal format
    """
    if isinstance(odds, float): # Nothing to convert
        return odds
    elif isinstance(odds, int): # Convert American to decimal
        if odds > 0:
            return (abs(odds / 100) + 1)
        elif odds < 0:
            return (abs(100 / odds) + 1)
    elif isinstance(odds, str): # Convert fractional to decimal
        odds = Fraction(odds)
        return float(odds + 1)
        
def convertToAmerican(odds: int|float|str) -> int:
    """
    :param: Odds (any format)
    :return: Odds in American format
    :usage: Convert odds to American format
    """
    if isinstance(odds, int): # Nothing to convert
        return odds
    elif isinstance(odds, float): # Convert decimal to American
        if odds >= 2.0:
            return int((odds - 1)*100)
        elif odds < 2.0:
            return int(-100/(odds - 1))
    elif isinstance(odds, str): # Convert fractional to American
        odds = Fraction(odds)
        if odds.numerator > odds.denominator:
            return int(odds * 100)
        elif odds.numerator < odds.denominator:
            return int(-100 / odds)

def convertToFractional(odds: int|float|str) -> Fraction:
    """
    :param: Odds (any format)
    :return: Odds in fractional format
    :usage: Convert odds to fractional format
    """
    if isinstance(odds, str): # Nothing to convert
        return odds
    elif isinstance(odds, float): # Convert deciaml to fractional
        odds = Fraction(odds - 1/ 1)
        if odds.denominator == 1:
            return (f'{odds}/1')
        else:
            return odds
    elif isinstance(odds, int): # Convert American to fractional
        odds = Fraction(odds/100)
        if odds.denominator == 1:
            return (f'{odds}/1')
        else:
            return odds

def calculateParlayOdds(odds: list, rounding: int = 2) -> float:
    """
    :param: List of odds (any format)
    :return: Overall parlay odds
    :usage: Calculate overall odds for a parlay
    """
    odds = list(map(convertToDecimal, odds))
    return round(math.prod(odds), rounding)

def calculateImpliedProbability(odds) -> float:
    """
    :param: Odds (any format)
    :return: Implied probability
    :usage: Calculate the implied probability for a given odd
    """
    odds = convertToDecimal(odds)
    impliedProbability = round(util.div(1, odds) * 100, 2)
    return (f'{impliedProbability}%')

def calculateTotalImpliedProbability(homeOdds: float, awayOdds: float, drawOdds: float = None) -> float:
    """
    :param: homeOdds, awayOdds, drawOdds (any format)
    :return: Total implied probability
    :usage: Calculate the implied probability for the given odds
    """
    homeOdds, awayOdds, drawOdds = convertToDecimal(homeOdds), convertToDecimal(awayOdds), convertToDecimal(drawOdds)
    total = 1/homeOdds + 1/awayOdds + util.div(1, drawOdds)
    total = round(total * 100, 2)
    return (f'{total}%')

def calculateVig(homeOdds: float, awayOdds: float, drawOdds: float = None) -> float:
    """
    :param: homeOdds, awayOdds, drawOdds (any format)
    :return: Vigorish
    :usage: Calculate the implied probability for the given odds
    """
    homeOdds, awayOdds, drawOdds = convertToDecimal(homeOdds), convertToDecimal(awayOdds), convertToDecimal(drawOdds)
    total = 1/homeOdds + 1/awayOdds + util.div(1, drawOdds)
    vig = round((total * 100) - 100, 2)
    return (f'{vig}%')