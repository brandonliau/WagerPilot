# Third party imports
from prettytable import PrettyTable
# Local imports
import wagerpilot.odds as odd
import wagerpilot.probability as prob
import wagerpilot.payout as pay

def castType(odds: str) -> int|float|str:
    if odds[0] in ('-', '+') or odds.isdigit():
        return int(odds)
    elif '.' in odds:
        return float(odds)
    return odds

def castListType(odds: list) -> list:
    for item in odds:
        index = odds.index(item)
        if item[0] in ('-', '+') or item.isdigit():
            odds[index] = int(item)
        elif '.' in item:
            odds[index] = float(item)
    return odds

def tableOdds(title: str, odds: int|float|str) -> PrettyTable:
    table = PrettyTable()
    table.title = title
    table.field_names = ['Format', 'Value']
    table.add_row(['Decimal', round(odd.toDecimal(odds), 2)])
    table.add_row(['American', odd.toAmerican(odds)])
    table.add_row(['Fractional', odd.toFractional(odds)])
    table.add_row(['Implied Probability', f'{round(prob.impliedProbability(odds) * 100, 2)}%'])
    table.align['Format'] = 'l'
    table.align['Value'] = 'r'
    return table

def tableVig(title: str, homeodds: int|float|str, awayodds: int|float|str, drawodds: int|float|str) -> PrettyTable:
    table = PrettyTable()
    table.title = title
    table.field_names = ['col1', 'col2']
    table.header = False
    table.add_row(['Total Implied Probability', f'{round(prob.totalImpliedProbability(homeodds, awayodds, drawodds) * 100, 2)}%'])
    table.add_row(['Vigorish', f'{round(odd.vig(homeodds, awayodds, drawodds) * 100, 2)}%'])
    table.align['col1'] = 'l'
    table.align['col2'] = 'r'
    return table

def tableTrue(title: str, homeodds: int|float|str, awayodds: int|float|str, drawodds: int|float|str):
    odds = odd.trueProability(homeodds, awayodds, drawodds)
    homeOdds, awayOdds, drawOdds = odds['homeTrue'], odds['awayTrue'], odds['drawTrue']
    table = PrettyTable()
    table.title = title
    table.field_names = ['col1', 'col2']
    table.header = False
    table.add_row(['Home Win Percentage', f'{round(homeOdds * 100, 2)}%'])
    table.add_row(['Away Win Percentage', f'{round(awayOdds * 100, 2)}%'])
    if drawOdds != 0:
        table.add_row(['Draw Percentage', f'{round(drawOdds * 100, 2)}%'])
    table.align['col1'] = 'l'
    table.align['col2'] = 'r'
    return table

def tableFair(title: str, homeodds: int|float|str, awayodds: int|float|str, drawodds: int|float|str) -> PrettyTable:
    odds = odd.fairOdds(homeodds, awayodds, drawodds)
    homeOdds, awayOdds, drawOdds = odds['homeFair'], odds['awayFair'], odds['drawFair']
    table = PrettyTable()
    table.title = title
    table.field_names = ['Format', 'Home Odds', 'Away Odds']
    table.add_row(['Decimal', round(odd.toDecimal(homeOdds), 2), round(odd.toDecimal(awayOdds), 2)])
    table.add_row(['American', odd.toAmerican(homeOdds), odd.toAmerican(awayOdds)])
    table.add_row(['Fractional', odd.toFractional(homeOdds), odd.toFractional(awayOdds)])
    table.add_row(['Implied Probability', f'{round(prob.impliedProbability(homeOdds) * 100, 2)}%', f'{round(prob.impliedProbability(awayOdds) * 100, 2)}%'])
    table.align['Format'] = 'l'
    table.align['Home Odds'] = 'r'
    table.align['Away Odds'] = 'r'
    if drawOdds != 0:
        table.add_column('Draw Odds', [round(odd.toDecimal(drawOdds), 2), odd.toAmerican(drawOdds), odd.toFractional(drawOdds), f'{round(prob.impliedProbability(drawOdds) * 100, 2)}%'])
        table.align['Draw Odds'] = 'r'
    return table

def tableStake(title: str, stake: float, odds: int|float|str) -> PrettyTable:
    table = PrettyTable()
    table.title = title
    table.field_names = ['col1', 'col2']
    table.header = False
    table.add_row(['Payout', f'${round(pay.payout(stake, odds), 2)}'])
    table.add_row(['Profit', f'${round(pay.profit(stake, odds), 2)}'])
    table.align['col1'] = 'l'
    table.align['col2'] = 'r'
    return table