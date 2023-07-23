Sports_Schema = {'key': 'americanfootball_ncaaf',
                 'group': ' American Football',
                 'title': 'NCAAF',
                 'description': 'US College Football'
                }

Events_Schema = {'id': 'bda33adca828c09dc3cac3a856aef176',
                'sport_key': 'americanfootball_nfl',
                'commence_date': '2023-07-25',
                'commence_time': '18:45:00',
                'home_team': 'Tampa Bay Buccaneers',
                'away_team': 'Dallas Cowboys',
                'home_odds': {'bookie_key': 1.5,
                              'bookie_key': 1.5,
                              'bookie_key': 1.5},
                'away_odds': {'bookie_key': 1.5,
                              'bookie_key': 1.5,
                              'bookie_key': 1.5},
                'draw_odds': {'bookie_key': 1.5,
                              'bookie_key': 1.5,
                              'bookie_key': 1.5}
                }

Best_Odds_Schema = {'id': 'bda33adca828c09dc3cac3a856aef176',
                    'sport_key': 'americanfootball_nfl',
                    'commence_date': '2023-07-25',
                    'commence_time': '18:45:00',
                    'home_team': 'Tampa Bay Buccaneers',
                    'away_team': 'Dallas Cowboys',
                    'best_home_odds': {'best': [1.5, 'bookie_key', 'bookie_key'],
                                       'us': [1.5, 'bookie_key', 'bookie_key'],
                                       'us2': [1.5, 'bookie_key', 'bookie_key'],
                                       'usk': [1.5, 'bookie_key', 'bookie_key'],
                                       'au': [1.5, 'bookie_key', 'bookie_key'],
                                       'eu': [1.5, 'bookie_key', 'bookie_key']},
                    'best_away_odds': {'best': [1.5, 'bookie_key', 'bookie_key'],
                                       'us': [1.5, 'bookie_key', 'bookie_key'],
                                       'us2': [1.5, 'bookie_key', 'bookie_key'],
                                       'usk': [1.5, 'bookie_key', 'bookie_key'],
                                       'au': [1.5, 'bookie_key', 'bookie_key'],
                                       'eu': [1.5, 'bookie_key', 'bookie_key']},
                    'best_draw_odds': {'best': [1.5, 'bookie_key', 'bookie_key'],
                                       'us': [1.5, 'bookie_key', 'bookie_key'],
                                       'us2': [1.5, 'bookie_key', 'bookie_key'],
                                       'usk': [1.5, 'bookie_key', 'bookie_key'],
                                       'au': [1.5, 'bookie_key', 'bookie_key'],
                                       'eu': [1.5, 'bookie_key', 'bookie_key']}
                    }

Completed_Events_Schema = {'id': 'bda33adca828c09dc3cac3a856aef176',
                           'sport_key': 'americanfootball_nfl',
                           'commence_date': '2023-07-25',
                           'commence_time': '18:45:00',
                           'home_team': 'Tampa Bay Buccaneers',
                           'away_team': 'Dallas Cowboys',
                           'home_team_score': '47',
                           'away_team_score': '25',
                           'outcome': 'home_team'
                           }
