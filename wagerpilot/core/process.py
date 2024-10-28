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
        meta=['id', 'home_team', 'away_team', 'commence_time', ['bookmakers', 'key']],
        errors='raise'
    )
    # Rename columns for clarity
    df.rename(columns={
        'bookmakers.key': 'bookmaker',
        'name': 'outcome_name',
        'price': 'outcome_price'}, 
        inplace=True
    )
    # Ensure the outcome prices are numeric
    df['outcome_price'] = pd.to_numeric(df['outcome_price'], errors='coerce')
    bookie_cols = list(df['bookmaker'].unique())

    # Create odds_df DataFrame
    odds_df = df.pivot(index=['id', 'outcome_name'], columns='bookmaker', values='outcome_price').reset_index()
    # Reorder DataFrame to match original df
    odds_df = odds_df.merge(df[['id', 'outcome_name']].drop_duplicates(), on=['id', 'outcome_name'], how='right')
    odds_df.columns.name = None

    # Create events_df DataFrame
    events_df = df[['id', 'commence_time', 'home_team', 'away_team']].drop_duplicates().reset_index(drop=True)
    events_df = events_df.merge(odds_df[['id', 'outcome_name'] + bookie_cols], on='id', how='left')
    # Create columns to store max home_odds, away_odds, and draw_odds
    events_df['home_odds'] = events_df.loc[events_df['outcome_name'] == events_df['home_team'], bookie_cols].max(axis=1)
    events_df['away_odds'] = events_df.loc[events_df['outcome_name'] == events_df['away_team'], bookie_cols].max(axis=1)
    events_df['draw_odds'] = events_df.loc[events_df['outcome_name'] == 'Draw', bookie_cols].max(axis=1)

    # Create a DataFrame that contains True where values match
    home_matches = events_df[bookie_cols].eq(events_df['home_odds'], axis=0)
    away_matches = events_df[bookie_cols].eq(events_df['away_odds'], axis=0)
    draw_matches = events_df[bookie_cols].eq(events_df['draw_odds'], axis=0)
    # Create columns to store bookmakers of max odds
    events_df['home_bookmaker'] = [home_matches.columns[row].tolist() for row in home_matches.to_numpy()]
    events_df['away_bookmaker'] = [away_matches.columns[row].tolist() for row in away_matches.to_numpy()]
    events_df['draw_bookmaker'] = [draw_matches.columns[row].tolist() for row in draw_matches.to_numpy()]
    # Replace empty lists with NaN in home_bookmaker, away_bookmaker, and draw_bookmaker
    max_bookie_cols = ['home_bookmaker', 'away_bookmaker', 'draw_bookmaker']
    events_df[max_bookie_cols] = events_df[max_bookie_cols].apply(lambda col: col.apply(lambda x: None if x == [] else x))

    # Merge rows with matching event id's and aggregate the home_odds, away_odds, and draw_odds data into a single row
    events_df = events_df.groupby('id').agg(lambda x: x.dropna().iloc[0] if not x.dropna().empty else None).reset_index()

    # Reorder DataFrame to match original df
    events_df = events_df.merge(df['id'].drop_duplicates(), on=['id'], how='right')
    # Drop extraneous columns (outcome_name and bookie_cols)
    events_df = events_df.drop(columns=['outcome_name'] + bookie_cols)
    # Create column to store implied probability
    events_df['implied_prob'] = events_df.apply(lambda x: totalImpliedProbability(x['home_odds'], x['away_odds'], x['draw_odds']), axis=1)
    # Create column to store whether event contains arbitrage opportunity
    events_df['arbitrage'] = events_df['implied_prob'] < 1

    return (events_df, odds_df)


# def clean_data(df: pd.DataFrame):
    