from fractions import Fraction
import math

def convertToDecimal(odds: int|float|str) -> float:
    """
    :param: Odds (any format)
    :return: Odds in decimal format
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
        
def calculateParlayOdds(odds: list) -> float:
    """
    :param: List of odds (any format)
    :return: Parlay odds in decimal format
    """
    odds = list(map(convertToDecimal, odds))
    return math.prod(odds)

def calculateImpliedProbability(odds) -> float:
    """
    :param: Odds (any format)
    :return: Implied probability
    """
    odds = convertToDecimal(odds)
    return (f'{(1/odds) * 100}%')
