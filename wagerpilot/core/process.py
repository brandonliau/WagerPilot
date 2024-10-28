# Third party imports
import pandas as pd
# Local imports
from wagerpilot.betting.probability import totalImpliedProbability

def process_h2h_data_deprecated(data: list) -> tuple:
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
            'implied_prob': totalImpliedProbability(best_home_odds, best_away_odds),
            'arbitrage': totalImpliedProbability(best_home_odds, best_away_odds) < 1.0,
        }
        if best_draw_odds != float('-inf'):
            event_data['draw_odds'] = best_draw_odds
            event_data['draw_bookmaker'] = draw_bookmaker
            event_data['implied_prob'] = totalImpliedProbability(best_home_odds, best_away_odds, best_draw_odds)
            event_data['arbitrage'] = totalImpliedProbability(best_home_odds, best_away_odds, best_draw_odds) < 1.0
        event_rows.append(event_data)

    return (pd.DataFrame(event_rows), pd.DataFrame(bookie_rows))

def process_h2h_data(data: list) -> tuple:
    # Flatten JSON data into a DataFrame
    df = pd.json_normalize(
        data,
        record_path=['bookmakers', 'markets', 'outcomes'],
        meta=['id', 'sport_key', 'home_team', 'away_team', 'commence_time', ['bookmakers', 'key']],
        errors='raise'
    )
    if df.empty:
        return None
    # Rename columns for clarity
    df.rename(columns={
        'bookmakers.key': 'bookmaker',
        'name': 'outcome_name',
        'price': 'outcome_price'}, 
        inplace=True
    )
    # Ensure the outcome prices are numeric
    df['outcome_price'] = pd.to_numeric(df['outcome_price'], errors='coerce')
    bookie_cols = df['bookmaker'].unique().tolist()
    
    # Create odds_df DataFrame
    odds_df = df.pivot(index=['id', 'outcome_name'], columns='bookmaker', values='outcome_price').reset_index()
    # Reorder DataFrame to match original df
    odds_df = odds_df.merge(df[['id', 'outcome_name']].drop_duplicates(), on=['id', 'outcome_name'], how='right')
    odds_df.columns.name = None

    # Create events_df DataFrame
    events_df = df[['id', 'sport_key', 'commence_time', 'home_team', 'away_team']].drop_duplicates().reset_index(drop=True)
    # Create columns to store max odds
    outcome_odds = odds_df.set_index(['id', 'outcome_name'])
    events_df['home_odds'] = events_df.apply(lambda x: outcome_odds.loc[(x['id'], x['home_team'])][bookie_cols].max() if (x['id'], x['home_team']) in outcome_odds.index else None, axis=1)
    events_df['away_odds'] = events_df.apply(lambda x: outcome_odds.loc[(x['id'], x['away_team'])][bookie_cols].max() if (x['id'], x['away_team']) in outcome_odds.index else None, axis=1)
    events_df['draw_odds'] = events_df.apply(lambda x: outcome_odds.loc[(x['id'], 'Draw')][bookie_cols].max() if (x['id'], 'Draw') in outcome_odds.index else None, axis=1)
    
    # Create columns to store bookmakers of max odds
    def get_max_bookmaker(row, outcome_name):
        if (row['id'], outcome_name) in outcome_odds.index:
            odds = outcome_odds.loc[(row['id'], outcome_name)][bookie_cols]
            return odds[odds == odds.max()].index.tolist() if not odds.isna().all() else None
        return None
    events_df['home_bookmaker'] = events_df.apply(lambda x: get_max_bookmaker(x, x['home_team']), axis=1)
    events_df['away_bookmaker'] = events_df.apply(lambda x: get_max_bookmaker(x, x['away_team']), axis=1)
    events_df['draw_bookmaker'] = events_df.apply(lambda x: get_max_bookmaker(x, 'Draw'), axis=1)
    
    # Create column to store implied probability
    events_df['implied_prob'] = events_df.apply(lambda x: totalImpliedProbability(x['home_odds'], x['away_odds'], x['draw_odds']), axis=1)
    # Create column to store whether event contains arbitrage opportunity
    events_df['arbitrage'] = events_df['implied_prob'] < 1

    # Drop draw_odds and draw_bookmaker if all values are NaN
    events_df = events_df.dropna(axis=1, how='all')

    return events_df, odds_df

# def clean_data(df: pd.DataFrame):
    