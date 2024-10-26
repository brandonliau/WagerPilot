# Standard library imports
import math
from fractions import Fraction

def toDecimal(odds: int|float|str) -> float:
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

def parlayOdds(odds: int|float|str) -> float:
    return math.prod(list(map(toDecimal, odds)))
