# Third party imports
import pandas as pd
# Local imports
from wagerpilot.tools.config_utils import Config
from wagerpilot.tools.api_utils import get_events
from wagerpilot.betting.probability import total_implied_probability

def process_spreads_data(data: list) -> tuple:
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
        'price': 'outcome_price',
        'point': 'spread_val'}, 
        inplace=True
    )
    # Ensure the outcome prices are numeric
    df['outcome_price'] = pd.to_numeric(df['outcome_price'], errors='coerce')
    df['spread_val'] = pd.to_numeric(df['spread_val'], errors='coerce')
    bookie_cols = df['bookmaker'].unique().tolist()

    # Create odds_df DataFrame
    odds_df = df.pivot(index=['id', 'outcome_name', 'spread_val'], columns='bookmaker', values='outcome_price').reset_index()

    # Reorder DataFrame to match original df
    odds_df = odds_df.merge(df[['id', 'outcome_name']].drop_duplicates(), on=['id', 'outcome_name'], how='right')
    odds_df.columns.name = None

    # Create events_df DataFrame
    events_df = df[['id', 'sport_key', 'commence_time', 'home_team', 'away_team']].drop_duplicates().reset_index(drop=True)
    # Create columns to store max odds
    outcome_odds = odds_df.set_index(['id', 'outcome_name'])

    # Merge all spread values into the events_df    
    spreads_df = outcome_odds.merge(events_df[['id', 'home_team', 'away_team']], on='id', how='left')[['id', 'spread_val']]
    spreads_df = spreads_df.assign(abs_spread_val = lambda x: x['spread_val'].abs())
    unique_spreads = spreads_df.drop_duplicates(subset=['id', 'abs_spread_val'])[['id', 'abs_spread_val']]
    unique_spreads = unique_spreads.rename(columns={'abs_spread_val': 'spread_val'})
    events_df = events_df.merge(unique_spreads, on='id', how='left')

    # Get the max odds for each id, outcome, and spread combination
    odds_df['max_odds'] = odds_df[bookie_cols].max(axis=1)
    max_odds = odds_df.groupby(['id', 'spread_val'])['max_odds'].max().reset_index()
    events_df['pos_spread_odds'] = events_df.merge(max_odds, on=['id', 'spread_val'], how='left')['max_odds']
    max_odds['spread_val'] = -max_odds['spread_val']
    events_df['neg_spread_odds'] = events_df.merge(max_odds, on=['id', 'spread_val'], how='left')['max_odds']
    odds_df.drop('max_odds', axis=1, inplace=True)

    outcome_odds = odds_df.set_index(['id', 'outcome_name', 'spread_val'])

    # Create columns to store bookmakers of max odds
    def get_max_bookmaker(row, spread_val):
        if (row['id'], row['home_team'], spread_val) in outcome_odds.index:
            # print('exist', row['id'], outcome_name, spread_val)
            odds = outcome_odds.loc[(row['id'], row['home_team'], spread_val)][bookie_cols]
            return odds[odds == odds.max()].index.tolist() if not odds.isna().all() else None
        elif (row['id'], row['away_team'], spread_val) in outcome_odds.index:
            odds = outcome_odds.loc[(row['id'], row['away_team'], spread_val)][bookie_cols]
            return odds[odds == odds.max()].index.tolist() if not odds.isna().all() else None
        return None
    events_df['pos_bookmakers'] = events_df.apply(lambda x: get_max_bookmaker(x, x['spread_val']), axis=1)
    events_df['neg_bookmakers'] = events_df.apply(lambda x: get_max_bookmaker(x, -x['spread_val']), axis=1)

    # Create column to store implied probability
    events_df['implied_prob'] = events_df.apply(lambda x: total_implied_probability(x['pos_spread_odds'], x['neg_spread_odds']), axis=1)
    # Create column to store whether event contains arbitrage opportunity
    events_df['arbitrage'] = events_df['implied_prob'] < 1

    return events_df, odds_df

def get_all_spreads_data(config: Config, sports: list) -> dict:
    all_spreads_data = {}
    for sport in sports:
        event_data = get_events(config, sport['key'], 'spreads')
        if not event_data:
            print(f"Invalid parameter combination : ['sport_key': {sport['key']}, 'market': 'spreads']")
            continue
        spreads_data = process_spreads_data(event_data)
        if not spreads_data:
            print(f"Missing bookmaker data : {event_data}")
            continue
        print(event_data)
        all_spreads_data[sport['key']] = spreads_data
    return all_spreads_data
