# SA20 Cricket Analysis - PowerBI Dashboard Guide

This guide will help you create an interactive PowerBI dashboard for SA20 cricket data analysis.

## Data Files Overview

1. `match_summary.csv`: Overall match statistics
2. `player_batting.csv`: Individual player batting performance
3. `venue_stats.csv`: Venue-specific statistics
4. `partnerships.csv`: Partnership analysis
5. `over_analysis.csv`: Over-by-over match progression
6. `team_stats.csv`: Team performance metrics
7. `powerplay_batting.csv`: Powerplay batting statistics
8. `powerplay_bowling.csv`: Powerplay bowling statistics

## Dashboard Structure

### Page 1: Match Overview
- **Visualizations:**
  1. Match Summary Table
     - Teams, Venue, Date, Total Runs, Wickets
  2. Match Timeline
     - Line chart showing match progression
  3. Venue Performance
     - Bar chart comparing venues
  4. Team Performance Metrics
     - Cards showing total runs, matches played, win rate

### Page 2: Player Analysis
- **Visualizations:**
  1. Top Batsmen
     - Bar chart of runs scored
     - Scatter plot of strike rate vs average
  2. Player Performance Trends
     - Line chart showing form over matches
  3. Partnership Analysis
     - Heat map of successful partnerships
  4. Player Statistics
     - Detailed table with filters

### Page 3: Powerplay Analysis
- **Visualizations:**
  1. Powerplay Performance
     - Bar chart comparing teams
  2. Top Powerplay Batsmen
     - Bar chart of runs in powerplay
  3. Powerplay Bowling
     - Bar chart of economy rates
  4. Powerplay Impact
     - Scatter plot of powerplay runs vs match result

### Page 4: Venue Analysis
- **Visualizations:**
  1. Venue Comparison
     - Bar chart of average runs per venue
  2. Venue Characteristics
     - Scatter plot of boundaries vs total runs
  3. Venue Timeline
     - Line chart showing venue performance over time
  4. Venue Statistics
     - Detailed table with filters

## Setting Up the Dashboard

1. **Import Data:**
   - Open PowerBI Desktop
   - Click "Get Data" > "Text/CSV"
   - Import all CSV files from the powerbi_data folder

2. **Create Relationships:**
   - Match ID → Match Summary
   - Player → Player Batting
   - Venue → Venue Stats
   - Team → Team Stats

3. **Create Measures:**
   ```dax
   // Example measures
   Total Matches = COUNTROWS('match_summary')
   Average Runs = AVERAGE('match_summary'[total_runs])
   Win Rate = DIVIDE([Wins], [Total Matches], 0)
   ```

4. **Design Tips:**
   - Use consistent color scheme
   - Add filters for date range, teams, and players
   - Include tooltips for detailed information
   - Use conditional formatting for important metrics

## Interactive Features

1. **Filters:**
   - Date range selector
   - Team filter
   - Player filter
   - Venue filter

2. **Drill-through:**
   - Match details
   - Player profiles
   - Venue statistics

3. **Tooltips:**
   - Detailed statistics on hover
   - Performance trends
   - Comparative analysis

## Best Practices

1. **Performance:**
   - Use calculated columns for frequently used metrics
   - Optimize relationships
   - Use appropriate data types

2. **Visualization:**
   - Keep it clean and uncluttered
   - Use appropriate chart types
   - Include clear labels and titles

3. **Interactivity:**
   - Add slicers for easy filtering
   - Include drill-through capabilities
   - Use bookmarks for different views

## Publishing

1. Save the PowerBI file (.pbix)
2. Publish to PowerBI Service
3. Share with stakeholders
4. Set up automatic refresh if needed

## Additional Resources

- [PowerBI Documentation](https://docs.microsoft.com/power-bi/)
- [DAX Reference](https://docs.microsoft.com/dax/)
- [PowerBI Community](https://community.powerbi.com/) 