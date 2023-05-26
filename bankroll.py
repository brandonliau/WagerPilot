import getData as data
import odds as odd

def mariaStaking(bankroll: float, odds: float):
    """
    :param: bankroll, odds
    :return: Amount to wager
    :usage: Calculate amount to wager given the odds for an event
    """
    odds = odd.toDecimal(odds)
    if odds <= 3.5:
        return (0.01 * bankroll) # Wager 1% of bankroll (odds <= 3.5)
    elif odds >= 3.6 or odds <= 7.4:
        return (0.006 * bankroll) # Wager 0.6% of bankroll (3.6 <= odds <= 7.4)
    elif odds >= 7.5 or odds <= 11:
        return (0.004 * bankroll) # Wager 0.4% of bankroll (7.5 <= odds <= 11)
    elif odds > 11:
        return ("Don't wager anything!" ) # Wager 0% of bankroll (odds > 11)
    
def kellyCriterion(bankroll: float, odds: float, confidence: float, kellyMultiplier: float = 1):
    """
    :param: bankroll, odds, confidence (eg. 0.6), kellyMultiplier (1: Full Kelly, 0.5: Half Kelly, 1+: Levered Kelly)
    :return: Amount to wager
    :usage: Calculate amount to wager given the odds for an event
    """
    b = odd.toDecimal(odds) - 1 # Decimal odds
    p = confidence # Probability of winning
    q = 1 - confidence # Probabilty of losing
    toWager = ((b * p - q) / b) * kellyMultiplier * bankroll
    return round(toWager, 2)