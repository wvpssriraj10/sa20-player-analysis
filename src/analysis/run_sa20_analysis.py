import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from cricket_analysis import CricketAnalyzer
import json
from datetime import datetime

def save_analysis_results():
    # Initialize the analyzer
    analyzer = CricketAnalyzer('all_matches.csv')
    
    # Create results directory if it doesn't exist
    results_dir = Path('analysis_results')
    results_dir.mkdir(exist_ok=True)
    
    # 1. Powerplay Analysis
    powerplay_batting, powerplay_bowling = analyzer.get_powerplay_stats()
    
    # Save powerplay batting stats
    powerplay_batting.to_csv(results_dir / 'powerplay_batting.csv', index=False)
    
    # Save powerplay bowling stats
    powerplay_bowling.to_csv(results_dir / 'powerplay_bowling.csv', index=False)
    
    # 2. Partnerships Analysis
    partnerships = analyzer.get_player_partnerships()
    partnerships.to_csv(results_dir / 'partnerships.csv', index=False)
    
    # 3. Venue Analysis
    venue_stats = analyzer.get_venue_analysis()
    venue_stats.to_csv(results_dir / 'venue_stats.csv', index=False)
    
    # 4. Generate visualizations
    # Powerplay batting strike rate distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data=powerplay_batting, x='powerplay_strike_rate', bins=20)
    plt.title('Distribution of Powerplay Strike Rates')
    plt.xlabel('Strike Rate')
    plt.ylabel('Count')
    plt.savefig(results_dir / 'powerplay_strike_rate_dist.png')
    plt.close()
    
    # Venue comparison
    plt.figure(figsize=(12, 6))
    sns.barplot(data=venue_stats, x='venue', y='avg_total_runs')
    plt.xticks(rotation=45)
    plt.title('Average Runs per Ball by Venue')
    plt.tight_layout()
    plt.savefig(results_dir / 'venue_comparison.png')
    plt.close()
    
    # 5. Save summary statistics
    summary = {
        'total_matches': len(analyzer.data['match_id'].unique()),
        'total_players': len(analyzer.data['striker'].unique()),
        'date_range': {
            'start': analyzer.data['start_date'].min().strftime('%Y-%m-%d'),
            'end': analyzer.data['start_date'].max().strftime('%Y-%m-%d')
        },
        'top_batsman': powerplay_batting.nlargest(1, 'powerplay_runs')['player'].iloc[0],
        'top_bowler': powerplay_bowling.nlargest(1, 'wickets')['player'].iloc[0],
        'highest_partnership': partnerships.nlargest(1, 'runs_off_bat')['runs_off_bat'].iloc[0],
        'highest_scoring_venue': venue_stats.nlargest(1, 'avg_total_runs')['venue'].iloc[0]
    }
    
    with open(results_dir / 'summary_stats.json', 'w') as f:
        json.dump(summary, f, indent=4)
    
    print("Analysis completed! Results saved in 'analysis_results' directory.")
    print("\nSummary Statistics:")
    print(f"Total Matches: {summary['total_matches']}")
    print(f"Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"Top Batsman: {summary['top_batsman']}")
    print(f"Top Bowler: {summary['top_bowler']}")
    print(f"Highest Partnership: {summary['highest_partnership']} runs")
    print(f"Highest Scoring Venue: {summary['highest_scoring_venue']}")

if __name__ == "__main__":
    save_analysis_results() 