# Third party imports
import pandas as pd
# Local imports
from wagerpilot.tools.config_utils import Config
from wagerpilot.tools.api_utils import get_events
from wagerpilot.math.probability import total_implied_probability

def process_totals_data(data: list) -> tuple:
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
        'point': 'totals_val'}, 
        inplace=True
    )
    # Ensure the outcome prices are numeric
    df['outcome_price'] = pd.to_numeric(df['outcome_price'], errors='coerce')
    df['totals_val'] = pd.to_numeric(df['totals_val'], errors='coerce')
    bookie_cols = df['bookmaker'].unique().tolist()

    # Create odds_df DataFrame
    odds_df = df.pivot(index=['id', 'outcome_name', 'totals_val'], columns='bookmaker', values='outcome_price').reset_index()

    # Reorder DataFrame to match original df
    odds_df = odds_df.merge(df[['id', 'outcome_name']].drop_duplicates(), on=['id', 'outcome_name'], how='right')
    odds_df.columns.name = None

    # Create events_df DataFrame
    events_df = df[['id', 'sport_key', 'commence_time', 'home_team', 'away_team']].drop_duplicates().reset_index(drop=True)
    # Create columns to store max odds
    outcome_odds = odds_df.set_index(['id', 'outcome_name'])

    # # Merge all spread values into the events_df    
    totals_df = outcome_odds.merge(events_df[['id']], on='id', how='left')[['id', 'totals_val']]
    unique_totals = totals_df.drop_duplicates(subset=['id', 'totals_val'])[['id', 'totals_val']]
    events_df = events_df.merge(unique_totals, on='id', how='left')

    # Get the max odds for each id, outcome, and spread combination
    odds_df['max_odds'] = odds_df[bookie_cols].max(axis=1)
    events_df['over_odds'] = events_df.merge(odds_df[odds_df['outcome_name'] == 'Over'], on=['id', 'totals_val'], how='left')['max_odds']
    events_df['under_odds'] = events_df.merge(odds_df[odds_df['outcome_name'] == 'Under'], on=['id', 'totals_val'], how='left')['max_odds']
    odds_df.drop('max_odds', axis=1, inplace=True)

    outcome_odds = odds_df.set_index(['id', 'outcome_name', 'totals_val'])

    # Create columns to store bookmakers of max odds
    def get_max_bookmaker(row, totals_val):
        if (row['id'], 'Over', totals_val) in outcome_odds.index:
            odds = outcome_odds.loc[(row['id'], 'Over', totals_val)][bookie_cols]
            return odds[odds == odds.max()].index.tolist() if not odds.isna().all() else None
        elif (row['id'], 'Under', totals_val) in outcome_odds.index:
            odds = outcome_odds.loc[(row['id'], 'Under', totals_val)][bookie_cols]
            return odds[odds == odds.max()].index.tolist() if not odds.isna().all() else None
        return None
    events_df['over_bookmakers'] = events_df.apply(lambda x: get_max_bookmaker(x, x['totals_val']), axis=1)
    events_df['under_bookmakers'] = events_df.apply(lambda x: get_max_bookmaker(x, -x['totals_val']), axis=1)

    # Create column to store implied probability
    events_df['implied_prob'] = events_df.apply(lambda x: total_implied_probability(x['over_odds'], x['under_odds']), axis=1)
    # Create column to store whether event contains arbitrage opportunity
    events_df['arbitrage'] = events_df['implied_prob'] < 1

    return events_df, odds_df

def process_all_totals_data(config: Config, sports: list) -> dict:
    all_spreads_data = {}
    for sport in sports:
        event_data = get_events(config, sport['key'], 'totals')
        if not event_data:
            print(f"Invalid parameter combination : ['sport_key': {sport['key']}, 'market': 'spreads']")
            continue
        spreads_data = process_totals_data(event_data)
        if not spreads_data:
            print(f"Missing bookmaker data : {event_data}")
            continue
        print(event_data)
        all_spreads_data[sport['key']] = spreads_data
    return all_spreads_data
