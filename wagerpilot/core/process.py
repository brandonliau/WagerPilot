# Third party imports
import pandas as pd
# Local imports
import wagerpilot.betting.probability as prob

def process_h2h_data(data: list) -> tuple:
    event_rows, bookie_rows = [], []
    
    for event in data:
        min_price, max_price = float('inf'), float('-inf')
        min_bookmaker, max_bookmaker = [], []
        event_id, home_team, away_team = event['id'], event['home_team'], event['away_team']

        for bookmaker in event['bookmakers']:
            home_odds, away_odds = None, None
            for outcome in bookmaker['markets'][0]['outcomes']:
                if outcome['name'] == home_team:
                    home_odds = outcome['price']
                if outcome['name'] == away_team:
                    away_odds = outcome['price']
                
                if outcome["price"] <= min_price:
                    if outcome["price"] < min_price:
                        min_bookmaker = [bookmaker['key']]
                    else:
                        min_bookmaker.append(bookmaker['key'])
                    min_price = outcome['price']
                if outcome['price'] >= max_price:
                    if outcome["price"] > max_price:
                        max_bookmaker = [bookmaker['key']]
                    else:
                        max_bookmaker.append(bookmaker['key'])
                    max_price = outcome['price']
                        
            bookie_rows.append({
                'event_id': event_id,
                'bookmaker': bookmaker['key'],
                'home_odds': home_odds,
                'away_odds': away_odds,
            })
            
        event_rows.append({
            'event_id': event_id,
            'home_team': home_team,
            'away_team': away_team,
            'min_price': min_price,
            'max_price': max_price,
            'min_price_bookmaker': min_bookmaker,
            'max_price_bookmaker': max_bookmaker,
            'arbitrage': (prob.impliedProbability(min_price) + prob.impliedProbability(max_price)) < 1.0,
        })

    return (pd.DataFrame(event_rows), pd.DataFrame(bookie_rows))
