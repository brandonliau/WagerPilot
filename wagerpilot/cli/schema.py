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
                'home_odds': {'bookie_key': [1.5, 'region'],
                              'bookie_key': [1.5, 'region'],
                              'bookie_key': [1.5, 'region']},
                'away_odds': {'bookie_key': [1.5, 'region'],
                              'bookie_key': [1.5, 'region'],
                              'bookie_key': [1.5, 'region']},
                'draw_odds': {'bookie_key': [1.5, 'region'],
                              'bookie_key': [1.5, 'region'],
                              'bookie_key': [1.5, 'region']}
                }

Best_Odds_Schema = {'id': 'bda33adca828c09dc3cac3a856aef176',
                    'home_team': 'Tampa Bay Buccaneers',
                    'away_team': 'Dallas Cowboys',
                    'best_home_odds': {'best': ['bookie_key', 1.5],
                                       'us': ['bookie_key', 1.5],
                                       'us2': ['bookie_key', 1.5],
                                       'usk': ['bookie_key', 1.5],
                                       'au': ['bookie_key', 1.5],
                                       'eu': ['bookie_key', 1.5]},
                    'best_away_odds': {'best': ['bookie_key': 1.5],
                                       'us': ['bookie_key', 1.5],
                                       'us2': ['bookie_key', 1.5],
                                       'usk': ['bookie_key', 1.5],
                                       'au': ['bookie_key', 1.5],
                                       'eu': ['bookie_key', 1.5]},
                    'best_draw_odds': {'best': ['bookie_key', 1.5],
                                       'us': ['bookie_key', 1.5],
                                       'us2': ['bookie_key', 1.5],
                                       'usk': ['bookie_key', 1.5],
                                       'au': ['bookie_key', 1.5],
                                       'eu': ['bookie_key', 1.5]}
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
