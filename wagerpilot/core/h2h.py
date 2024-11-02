# Third party imports
import pandas as pd
# Local imports
from wagerpilot.tools.config_utils import Config
from wagerpilot.tools.api_utils import get_events
from wagerpilot.betting.probability import total_implied_probability

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
    events_df['implied_prob'] = events_df.apply(lambda x: total_implied_probability(x['home_odds'], x['away_odds'], x['draw_odds']), axis=1)
    # Create column to store whether event contains arbitrage opportunity
    events_df['arbitrage'] = events_df['implied_prob'] < 1

    # Drop draw_odds and draw_bookmaker if all values are NaN
    events_df = events_df.dropna(axis=1, how='all')

    return events_df, odds_df

def get_all_h2h_data(config: Config, sports: list) -> dict:
    all_h2h_data = {}
    for sport in sports:
        event_data = get_events(config, sport['key'], 'h2h')
        if not event_data:
            print(f"Invalid parameter combination : ['sport_key': {sport['key']}, 'market': 'h2h']")
            continue
        h2h_data = process_h2h_data(event_data)
        if not h2h_data:
            print(f"Missing bookmaker data : {event_data}")
            continue
        print(event_data)
        all_h2h_data[sport['key']] = h2h_data
    return all_h2h_data
