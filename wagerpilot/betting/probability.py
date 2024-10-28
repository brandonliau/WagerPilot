# Local imports
from wagerpilot.betting.odds import to_decimal

def div(x: float, y: float) -> float:
    try:
        return x/y
    except (TypeError, ZeroDivisionError):
        return 0

def implied_probability(odds: int|float|str) -> float:
    return div(1, to_decimal(odds))

def total_implied_probability(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> float:
    return implied_probability(homeOdds) + implied_probability(awayOdds) + implied_probability(drawOdds)

def vig(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> float:
    return (total_implied_probability(homeOdds, awayOdds, drawOdds) - 1)

def true_proability(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> dict:
    total = total_implied_probability(homeOdds, awayOdds, drawOdds)
    homeOdds, awayOdds, drawOdds = to_decimal(homeOdds), to_decimal(awayOdds), to_decimal(drawOdds) 
    homeTrue = (1 / homeOdds) / total
    awayTrue = (1 / awayOdds) / total
    drawTrue = (div(1, drawOdds)) / total
    return {'homeTrue': homeTrue, 'awayTrue': awayTrue, 'drawTrue': drawTrue}

def fair_odds(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> dict:
    trueProb = true_proability(homeOdds, awayOdds, drawOdds)
    homeFair = 1 / trueProb['homeTrue']
    awayFair = 1 / trueProb['awayTrue']
    drawFair = div(1, trueProb['drawTrue'])
    return {'homeFair': homeFair, 'awayFair': awayFair, 'drawFair': drawFair}
