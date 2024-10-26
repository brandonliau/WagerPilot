# Local imports
import wagerpilot.betting.odds as odd

def div(x: float, y: float) -> float:
    try:
        return x/y
    except (TypeError, ZeroDivisionError):
        return 0

def impliedProbability(odds: int|float|str) -> float:
    return div(1, odd.toDecimal(odds))

def totalImpliedProbability(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> float:
    return impliedProbability(homeOdds) + impliedProbability(awayOdds) + impliedProbability(drawOdds)

def vig(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> float:
    return (totalImpliedProbability(homeOdds, awayOdds, drawOdds) - 1)

def trueProability(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> dict:
    total = totalImpliedProbability(homeOdds, awayOdds, drawOdds)
    homeOdds, awayOdds, drawOdds = odd.toDecimal(homeOdds), odd.toDecimal(awayOdds), odd.toDecimal(drawOdds) 
    homeTrue = (1 / homeOdds) / total
    awayTrue = (1 / awayOdds) / total
    drawTrue = (div(1, drawOdds)) / total
    return {'homeTrue': homeTrue, 'awayTrue': awayTrue, 'drawTrue': drawTrue}

def fairOdds(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> dict:
    trueProb = trueProability(homeOdds, awayOdds, drawOdds)
    homeFair = 1 / trueProb['homeTrue']
    awayFair = 1 / trueProb['awayTrue']
    drawFair = div(1, trueProb['drawTrue'])
    return {'homeFair': homeFair, 'awayFair': awayFair, 'drawFair': drawFair}
