# Third party imports
import pandas as pd
# Local imports
import wagerpilot.betting.probability as prob

def process_h2h_data(data: list) -> tuple:
    event_rows, bookie_rows = [], []
    
    for event in data:
        best_home_odds, best_away_odds, best_draw_odds = float('-inf'), float('-inf'), float('-inf')
        home_bookmaker, away_bookmaker, draw_bookmaker = [], [], []
        event_id, home_team, away_team = event['id'], event['home_team'], event['away_team']

        if not event['bookmakers']:
            continue

        for bookmaker in event['bookmakers']:
            bookie_data = {'event_id': event_id, 'bookmaker': bookmaker['key']}
            home_odds, away_odds, draw_odds = None, None, None
            for outcome in bookmaker['markets'][0]['outcomes']:
                if outcome['name'] == home_team:
                    home_odds = outcome['price']
                    bookie_data['home_odds'] = home_odds
                    if home_odds >= best_home_odds:
                        if home_odds > best_home_odds:
                            home_bookmaker = [bookmaker['key']]
                        else:
                            home_bookmaker.append(bookmaker['key'])
                        best_home_odds = home_odds
                if outcome['name'] == away_team:
                    away_odds = outcome['price']
                    bookie_data['away_odds'] = away_odds
                    if away_odds >= best_away_odds:
                        if away_odds > best_away_odds:
                            away_bookmaker = [bookmaker['key']]
                        else:
                            away_bookmaker.append(bookmaker['key'])
                        best_away_odds = away_odds
                if outcome['name'] == 'Draw':
                    draw_odds = outcome['price']
                    bookie_data['draw_odds'] = draw_odds
                    if draw_odds >= best_draw_odds:
                        if draw_odds > best_draw_odds:
                            draw_bookmaker = [bookmaker['key']]
                        else:
                            draw_bookmaker.append(bookmaker['key'])
                        best_draw_odds = draw_odds
            bookie_rows.append(bookie_data)
        
        event_data = {
            'event_id': event_id,
            'commence_time': event['commence_time'],
            'home_team': home_team,
            'away_team': away_team,
            'home_odds': best_home_odds,
            'away_odds': best_away_odds,
            'home_bookmaker': home_bookmaker,
            'away_bookmaker': away_bookmaker,
            'implied_prob': prob.totalImpliedProbability(best_home_odds, best_away_odds),
            'arbitrage': prob.totalImpliedProbability(best_home_odds, best_away_odds) < 1.0,
        }
        if best_draw_odds != float('-inf'):
            event_data['draw_odds'] = best_draw_odds
            event_data['draw_bookmaker'] = draw_bookmaker
            event_data['implied_prob'] = prob.totalImpliedProbability(best_home_odds, best_away_odds, best_draw_odds)
            event_data['arbitrage'] = prob.totalImpliedProbability(best_home_odds, best_away_odds, best_draw_odds) < 1.0
        event_rows.append(event_data)

    return (pd.DataFrame(event_rows), pd.DataFrame(bookie_rows))


# def clean_data(df: pd.DataFrame):
    