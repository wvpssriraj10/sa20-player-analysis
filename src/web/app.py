from flask import Flask, render_template, jsonify
import os
from data_processing.data_loader import load_data
from data_processing.data_processor import process_data

app = Flask(__name__)

# Load and process data
matches_df, players_df, teams_df = load_data()
processed_data = process_data(matches_df, players_df, teams_df)

@app.route('/')
def index():
    return render_template('index.html', 
                         overview_stats=processed_data['overview_stats'],
                         team_stats=processed_data['team_stats'],
                         recent_matches=processed_data['recent_matches'])

@app.route('/teams')
def teams():
    return render_template('teams.html', 
                         teams=processed_data['team_stats'])

@app.route('/team/<team_name>')
def team_details(team_name):
    team_data = processed_data['team_stats'].get(team_name, {})
    return render_template('team_details.html',
                         team_name=team_name,
                         team_data=team_data)

@app.route('/players')
def players():
    return render_template('players.html',
                         players=processed_data['player_stats'])

@app.route('/player/<player_name>')
def player_details(player_name):
    player_data = processed_data['player_stats'].get(player_name, {})
    return render_template('player_details.html',
                         player_name=player_name,
                         player_data=player_data)

# For Vercel: export the app as 'app' (do not overwrite it)
# For local: run as usual
if __name__ == '__main__':
    app.run(debug=True) 