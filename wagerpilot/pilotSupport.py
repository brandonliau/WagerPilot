# Third party imports
from prettytable import PrettyTable
# Local imports
import wagerpilot.odds as odd

def castType(odds: str) -> int|float|str:
    if odds[0] in ('-', '+') or odds.isdigit():
        return int(odds)
    elif '.' in odds:
        return float(odds)
    else:
        return odds

def castListType(odds: list) -> list:
    for item in odds:
        index = odds.index(item)
        if item[0] in ('-', '+') or item.isdigit():
            odds[index] = int(item)
        elif '.' in item:
            odds[index] = float(item)
    return odds

def createOdds(title: str, odds: int|float|str) -> PrettyTable:
    table = PrettyTable()
    table.title = title
    table.field_names = ['Format', 'Value']
    table.add_row(['Decimal', round(odd.toDecimal(odds), 2)])
    table.add_row(['American', odd.toAmerican(odds)])
    table.add_row(['Fractional', odd.toFractional(odds)])
    table.add_row(['Implied Probability', f'{round(odd.impliedProbability(odds) * 100, 2)}%'])
    table.align['Format'] = 'l'
    table.align['Value'] = 'r'
    return table

def createVig(title: str, homeodds: int|float|str, awayodds: int|float|str, drawodds: int|float|str) -> PrettyTable:
    table = PrettyTable()
    table.title = title
    table.header = False
    table.add_row(['Total Implied Probability', f'{round(odd.totalImpliedProbability(homeodds, awayodds, drawodds) * 100, 2)}%'])
    table.add_row(['Vigorish', f'{round(odd.vig(homeodds, awayodds, drawodds) * 100, 2)}%'])
    table.align['Format'] = 'l'
    table.align['Value'] = 'r'
    return table

def createFair(title: str, homeodds: int|float|str, awayodds: int|float|str, drawodds: int|float|str) -> PrettyTable:
    odds = odd.fairOdds(homeodds, awayodds, drawodds)
    homeOdds, awayOdds, drawOdds = odds['homeFair'], odds['awayFair'], odds['drawFair']
    
    table = PrettyTable()
    table.title = title
    table.field_names = ['Format', 'Home Odds', 'Away Odds']

    table.add_row(['Decimal', round(odd.toDecimal(homeOdds), 2), round(odd.toDecimal(awayOdds), 2)])
    table.add_row(['American', odd.toAmerican(homeOdds), odd.toAmerican(awayOdds)])
    table.add_row(['Fractional', odd.toFractional(homeOdds), odd.toFractional(awayOdds)])
    table.add_row(['Implied Probability', f'{round(odd.impliedProbability(homeOdds) * 100, 2)}%', f'{round(odd.impliedProbability(awayOdds) * 100, 2)}%'])

    table.align['Format'] = 'l'
    table.align['Home Odds'] = 'r'
    table.align['Away Odds'] = 'r'
    
    if drawOdds != 0:
        table.add_column('Draw Odds', [round(odd.toDecimal(drawOdds), 2), odd.toAmerican(drawOdds), odd.toFractional(drawOdds), f'{round(odd.impliedProbability(drawOdds) * 100, 2)}%'])
        table.align['Draw Odds'] = 'r'
    return table
