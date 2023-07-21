# Standard library imports
from fractions import Fraction
from decimal import Decimal
import math
# Local imports
import wagerpilot.utils as util

def toDecimal(odds: int|float|str) -> float:
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
        return float(Fraction(odds) + 1)
        
def toAmerican(odds: int|float|str) -> str:
    """
    :param: Odds (any format)
    :return: Odds in American format
    :usage: Convert odds to American format
    """
    if isinstance(odds, int): # Nothing to convert
        pass
    elif isinstance(odds, float): # Convert decimal to American
        if odds >= 2.0:
            odds = int((odds - 1) * 100)
        elif odds < 2.0:
            odds = int(-100 / (odds - 1))
    elif isinstance(odds, str): # Convert fractional to American
        odds = Fraction(odds)
        if odds.numerator > odds.denominator:
            odds = int((odds.numerator / odds.denominator) * 100)
        elif odds.numerator < odds.denominator:
            odds = int(-100 / (odds.numerator / odds.denominator))
    if odds > 0:
        return(f'+{odds}')
    return(f'{odds}')

def toFractional(odds: int|float|str) -> Fraction:
    """
    :param: Odds (any format)
    :return: Odds in fractional format
    :usage: Convert odds to fractional format
    """
    if isinstance(odds, str): # Nothing to convert
        return odds
    elif isinstance(odds, float): # Convert decimal to fractional
        odds = int((odds - 1) * 100)
        gcd = math.gcd(odds, 100)
        odds = Fraction(int(odds / gcd), int(100 / gcd))
    elif isinstance(odds, int): # Convert American to fractional
        odds = Fraction(odds / 100) if odds > 0 else Fraction(-100 / odds).limit_denominator()
    if odds.denominator == 1:
        return (f'{odds}/1')
    return odds

def impliedProbability(odds: int|float|str) -> float:
    """
    :param: Odds (any format)
    :return: Implied probability
    :usage: Calculate the implied probability for a given odd
    """
    return util.div(1, toDecimal(odds))

def parlayOdds(odds: int|float|str) -> float:
    """
    :param: List of odds (any format)
    :return: Overall parlay odds
    :usage: Calculate overall odds for a parlay
    """
    return math.prod(list(map(toDecimal, odds)))
    
def totalImpliedProbability(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> float:
    """
    :param: homeOdds, awayOdds, drawOdds (any format)
    :return: Total implied probability
    :usage: Calculate the implied probability for the given odds
    """
    return impliedProbability(homeOdds) + impliedProbability(awayOdds) + impliedProbability(drawOdds)

def vig(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> float:
    """
    :param: homeOdds, awayOdds, drawOdds (any format)
    :return: Vigorish
    :usage: Calculate the vig for the given odds
    """
    return (totalImpliedProbability(homeOdds, awayOdds, drawOdds) - 1)

def trueProability(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> dict:
    """
    :param: homeOdds, awayOdds, drawOdds (any format)
    :return: True proabability of each event
    :usage: Calculate the true probability of each event happen for the given odds
    """
    total = totalImpliedProbability(homeOdds, awayOdds, drawOdds)
    homeOdds, awayOdds, drawOdds = toDecimal(homeOdds), toDecimal(awayOdds), toDecimal(drawOdds) 
    homeTrue = (1 / homeOdds) / total
    awayTrue = (1 / awayOdds) / total
    drawTrue = (util.div(1, drawOdds)) / total
    return {'homeTrue': homeTrue, 'awayTrue': awayTrue, 'drawTrue': drawTrue}

def fairOdds(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> dict:
    """
    :param: homeOdds, awayOdds, drawOdds (any format)
    :return: Fair odds of each event
    :usage: Calculate the fair odds for the given odds
    """
    trueProb = trueProability(homeOdds, awayOdds, drawOdds)
    homeFair = 1 / trueProb['homeTrue']
    awayFair = 1 / trueProb['awayTrue']
    drawFair = util.div(1, trueProb['drawTrue'])
    return {'homeFair': homeFair, 'awayFair': awayFair, 'drawFair': drawFair}