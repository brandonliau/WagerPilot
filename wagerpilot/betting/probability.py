# Local imports
import wagerpilot.tools.utils as util
import wagerpilot.betting.odds as odd

def impliedProbability(odds: int|float|str) -> float:
    """
    :param: Odds (any format)
    :return: Implied probability
    :usage: Calculate the implied probability for the given odds
    """
    return util.div(1, odd.toDecimal(odds))

def totalImpliedProbability(homeOdds: int|float|str, awayOdds: int|float|str, drawOdds: int|float|str = None) -> float:
    """
    :param: homeOdds, awayOdds, drawOdds (any format)
    :return: Total implied probability
    :usage: Calculate the total implied probability for the given odds
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
    :usage: Calculate the true probability of an event happening based on the given odds
    """
    total = totalImpliedProbability(homeOdds, awayOdds, drawOdds)
    homeOdds, awayOdds, drawOdds = odd.toDecimal(homeOdds), odd.toDecimal(awayOdds), odd.toDecimal(drawOdds) 
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