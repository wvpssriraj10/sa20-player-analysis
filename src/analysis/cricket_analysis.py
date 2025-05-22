import pandas as pd
import matplotlib.pyplot as plt

class CricketAnalyzer:
    def __init__(self, data_path):
        """Initialize the analyzer with the data path."""
        self.data = pd.read_csv(data_path)
        self.data['start_date'] = pd.to_datetime(self.data['start_date'], format='%d-%m-%Y')
        
    def get_powerplay_stats(self):
        """Analyze powerplay (first 6 overs) performance."""
        powerplay_data = self.data[self.data['ball'] <= 6.0]
        
        # Batting in powerplay
        powerplay_batting = powerplay_data.groupby('striker').agg({
            'runs_off_bat': ['sum', 'count'],
            'match_id': 'nunique'
        }).reset_index()
        
        powerplay_batting.columns = ['player', 'powerplay_runs', 'powerplay_balls', 'matches']
        powerplay_batting['powerplay_strike_rate'] = (powerplay_batting['powerplay_runs'] / powerplay_batting['powerplay_balls'] * 100).round(2)
        
        # Bowling in powerplay
        powerplay_bowling = powerplay_data.groupby('bowler').agg({
            'runs_off_bat': 'sum',
            'extras': 'sum',
            'ball': 'count',
            'wicket_type': lambda x: (x != '0').sum()
        }).reset_index()
        
        powerplay_bowling.columns = ['player', 'runs_conceded', 'extras', 'balls_bowled', 'wickets']
        powerplay_bowling['powerplay_economy'] = ((powerplay_bowling['runs_conceded'] + powerplay_bowling['extras']) / 
                                                (powerplay_bowling['balls_bowled'] / 6)).round(2)
        
        return powerplay_batting, powerplay_bowling
    
    def get_player_partnerships(self, min_balls=10):
        """Analyze batting partnerships."""
        partnerships = self.data.groupby(['match_id', 'batting_team', 'striker', 'non_striker']).agg({
            'runs_off_bat': 'sum',
            'ball': 'count'
        }).reset_index()
        
        # Filter partnerships with minimum balls
        partnerships = partnerships[partnerships['ball'] >= min_balls]
        
        # Calculate partnership runs per ball
        partnerships['runs_per_ball'] = (partnerships['runs_off_bat'] / partnerships['ball']).round(2)
        
        return partnerships.sort_values('runs_off_bat', ascending=False)
    
    def get_venue_analysis(self):
        """Analyze venue-specific statistics."""
        venue_stats = self.data.groupby('venue').agg({
            'match_id': 'nunique',
            'runs_off_bat': 'mean',
            'extras': 'mean',
            'wicket_type': lambda x: (x != '0').mean()
        }).reset_index()
        
        venue_stats.columns = ['venue', 'matches_played', 'avg_runs_per_ball', 'avg_extras_per_ball', 'avg_wickets_per_ball']
        venue_stats['avg_total_runs'] = (venue_stats['avg_runs_per_ball'] + venue_stats['avg_extras_per_ball']).round(2)
        
        return venue_stats.sort_values('avg_total_runs', ascending=False)
    
    def get_player_form(self, player_name, window=5):
        """Analyze player's recent form."""
        player_matches = self.data[self.data['striker'] == player_name]['match_id'].unique()
        recent_matches = player_matches[-window:]
        
        recent_stats = self.data[
            (self.data['match_id'].isin(recent_matches)) & 
            (self.data['striker'] == player_name)
        ].groupby('match_id').agg({
            'runs_off_bat': 'sum',
            'ball': 'count'
        }).reset_index()
        
        recent_stats['strike_rate'] = (recent_stats['runs_off_bat'] / recent_stats['ball'] * 100).round(2)
        recent_stats['date'] = recent_stats['match_id'].map(
            self.data.groupby('match_id')['start_date'].first()
        )
        
        return recent_stats.sort_values('date')
    
    def get_match_momentum(self, match_id):
        """Analyze match momentum and key moments."""
        match_data = self.data[self.data['match_id'] == match_id].copy()
        match_data['over'] = match_data['ball'].apply(lambda x: int(x))
        
        # Calculate run rate per over
        run_rates = match_data.groupby(['innings', 'over']).agg({
            'runs_off_bat': 'sum',
            'extras': 'sum'
        }).reset_index()
        
        run_rates['total_runs'] = run_rates['runs_off_bat'] + run_rates['extras']
        run_rates['cumulative_runs'] = run_rates.groupby('innings')['total_runs'].cumsum()
        
        # Identify key moments (wickets, boundaries)
        key_moments = match_data[
            (match_data['runs_off_bat'].isin([4, 6])) | 
            (match_data['wicket_type'] != '0')
        ][['innings', 'over', 'ball', 'striker', 'runs_off_bat', 'wicket_type']]
        
        return run_rates, key_moments
    
    def get_player_matchup_stats(self, batsman, bowler):
        """Analyze head-to-head statistics between a batsman and bowler."""
        matchup_data = self.data[
            (self.data['striker'] == batsman) & 
            (self.data['bowler'] == bowler)
        ]
        
        if len(matchup_data) == 0:
            return None
        
        stats = {
            'balls_faced': len(matchup_data),
            'runs_scored': matchup_data['runs_off_bat'].sum(),
            'wickets': (matchup_data['wicket_type'] != '0').sum(),
            'boundaries': len(matchup_data[matchup_data['runs_off_bat'].isin([4, 6])]),
            'dot_balls': len(matchup_data[matchup_data['runs_off_bat'] == 0])
        }
        
        stats['strike_rate'] = (stats['runs_scored'] / stats['balls_faced'] * 100).round(2)
        stats['boundary_percentage'] = (stats['boundaries'] / stats['balls_faced'] * 100).round(2)
        
        return stats
    
    def plot_match_momentum(self, match_id):
        """Plot match momentum graph."""
        run_rates, key_moments = self.get_match_momentum(match_id)
        
        plt.figure(figsize=(15, 8))
        for innings in [1, 2]:
            innings_data = run_rates[run_rates['innings'] == innings]
            plt.plot(innings_data['over'], innings_data['cumulative_runs'], 
                    marker='o', label=f'Innings {innings}')
            
            # Plot key moments
            moments = key_moments[key_moments['innings'] == innings]
            for _, moment in moments.iterrows():
                if moment['wicket_type'] != '0':
                    plt.scatter(moment['over'], run_rates[
                        (run_rates['innings'] == innings) & 
                        (run_rates['over'] == moment['over'])
                    ]['cumulative_runs'].iloc[0], 
                    color='red', marker='x', s=100)
                elif moment['runs_off_bat'] in [4, 6]:
                    plt.scatter(moment['over'], run_rates[
                        (run_rates['innings'] == innings) & 
                        (run_rates['over'] == moment['over'])
                    ]['cumulative_runs'].iloc[0], 
                    color='green', marker='*', s=100)
        
        plt.title(f'Match Momentum - Match ID: {match_id}')
        plt.xlabel('Over')
        plt.ylabel('Cumulative Runs')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def plot_player_form(self, player_name, window=5):
        """Plot player's recent form."""
        form_data = self.get_player_form(player_name, window)
        
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(form_data)), form_data['strike_rate'], marker='o')
        plt.title(f'{player_name}\'s Recent Form (Last {window} Matches)')
        plt.xlabel('Match Number')
        plt.ylabel('Strike Rate')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    # Initialize the analyzer
    analyzer = CricketAnalyzer('all_matches.csv')
    
    # Example usage of new features
    print("\nPowerplay Analysis:")
    powerplay_batting_main, powerplay_bowling_main = analyzer.get_powerplay_stats()
    print("\nTop Powerplay Batsmen:")
    print(powerplay_batting_main.sort_values('powerplay_runs', ascending=False).head())
    print("\nTop Powerplay Bowlers:")
    print(powerplay_bowling_main.sort_values('wickets', ascending=False).head())
    
    print("\nTop Partnerships:")
    print(analyzer.get_player_partnerships().head())
    
    print("\nVenue Analysis:")
    print(analyzer.get_venue_analysis())
    
    # Example of player form analysis
    print("\nPlayer Form Analysis (example for first player in dataset):")
    first_player = analyzer.data['striker'].iloc[0]
    print(analyzer.get_player_form(first_player))
    
    # Example of match momentum analysis
    first_match = analyzer.data['match_id'].iloc[0]
    print(f"\nMatch Momentum Analysis for Match {first_match}:")
    run_rates_main, key_moments_main = analyzer.get_match_momentum(first_match)
    print("\nRun Rates:")
    print(run_rates_main)
    print("\nKey Moments:")
    print(key_moments_main)