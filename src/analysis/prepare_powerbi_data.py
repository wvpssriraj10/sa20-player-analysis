import pandas as pd
import numpy as np
from pathlib import Path
from cricket_analysis import CricketAnalyzer

def prepare_powerbi_data():
    # Initialize the analyzer
    analyzer = CricketAnalyzer('all_matches.csv')
    
    # Create PowerBI data directory
    powerbi_dir = Path('powerbi_data')
    powerbi_dir.mkdir(exist_ok=True)
    
    # 1. Match Summary Data
    match_summary = analyzer.data.groupby('match_id').agg({
        'start_date': 'first',
        'venue': 'first',
        'batting_team': lambda x: list(set(x)),
        'bowling_team': lambda x: list(set(x)),
        'runs_off_bat': 'sum',
        'extras': 'sum',
        'wicket_type': lambda x: (x != '0').sum()
    }).reset_index()
    
    match_summary['total_runs'] = match_summary['runs_off_bat'] + match_summary['extras']
    match_summary['teams'] = match_summary.apply(lambda x: ' vs '.join(sorted(set(x['batting_team'] + x['bowling_team']))), axis=1)
    match_summary.to_csv(powerbi_dir / 'match_summary.csv', index=False)
    
    # 2. Player Performance Data
    player_batting = analyzer.data.groupby('striker').agg({
        'runs_off_bat': ['sum', 'count'],
        'match_id': 'nunique',
        'ball': lambda x: (x <= 6.0).sum()  # Powerplay balls
    }).reset_index()
    
    player_batting.columns = ['player', 'total_runs', 'balls_faced', 'matches_played', 'powerplay_balls']
    player_batting['strike_rate'] = (player_batting['total_runs'] / player_batting['balls_faced'] * 100).round(2)
    player_batting['average'] = (player_batting['total_runs'] / player_batting['matches_played']).round(2)
    player_batting.to_csv(powerbi_dir / 'player_batting.csv', index=False)
    
    # 3. Venue Analysis Data
    venue_stats = analyzer.get_venue_analysis()
    venue_stats.to_csv(powerbi_dir / 'venue_stats.csv', index=False)
    
    # 4. Partnership Data
    partnerships = analyzer.get_player_partnerships()
    partnerships.to_csv(powerbi_dir / 'partnerships.csv', index=False)
    
    # 5. Over-by-Over Analysis
    analyzer.data['over_number'] = analyzer.data['ball'].apply(lambda x: int(x))
    over_analysis = analyzer.data.groupby(['match_id', 'innings', 'over_number']).agg({
        'runs_off_bat': 'sum',
        'extras': 'sum',
        'wicket_type': lambda x: (x != '0').sum()
    }).reset_index()
    
    over_analysis['total_runs'] = over_analysis['runs_off_bat'] + over_analysis['extras']
    over_analysis.to_csv(powerbi_dir / 'over_analysis.csv', index=False)
    
    # 6. Team Performance
    team_stats = analyzer.data.groupby('batting_team').agg({
        'match_id': 'nunique',
        'runs_off_bat': 'sum',
        'extras': 'sum',
        'wicket_type': lambda x: (x != '0').sum()
    }).reset_index()
    
    team_stats['total_runs'] = team_stats['runs_off_bat'] + team_stats['extras']
    team_stats['matches_played'] = team_stats['match_id']
    team_stats.to_csv(powerbi_dir / 'team_stats.csv', index=False)
    
    # 7. Powerplay Analysis
    powerplay_batting, powerplay_bowling = analyzer.get_powerplay_stats()
    powerplay_batting.to_csv(powerbi_dir / 'powerplay_batting.csv', index=False)
    powerplay_bowling.to_csv(powerbi_dir / 'powerplay_bowling.csv', index=False)
    
    print("PowerBI data preparation completed! Files saved in 'powerbi_data' directory.")

if __name__ == "__main__":
    prepare_powerbi_data() 