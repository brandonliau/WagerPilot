from fractions import Fraction
import math

def convertToDecimal(odds: int|float|str) -> float:
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
        
def calculateParlay(odds: list) -> float:
    return math.prod(odds)

def calculatePayout(stake: float, odds: int|float|str) -> float:
    odds = convertToDecimal(odds)
    return (odds * stake)

def calculateProfit(stake: float, odds: int|float|str) -> float:
    payout = calculatePayout(stake, odds)
    return (payout - stake)

def calculateImpliedProbability(odds) -> float:
    odds = convertToDecimal(odds)
    return (f'{(1/odds) * 100}%')
