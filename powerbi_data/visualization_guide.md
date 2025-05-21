# SA20 Cricket Analysis - PowerBI Visualization Guide

## Page 1: Match Overview

### 1. Match Summary Table
- **Type**: Table
- **Fields**:
  - Teams (from match_summary[teams])
  - Venue (from match_summary[venue])
  - Date (from match_summary[start_date])
  - Total Runs (from match_summary[total_runs])
  - Wickets (from match_summary[wicket_type])
- **Formatting**:
  - Conditional formatting for total_runs (green > 160, yellow > 140, red < 140)
  - Sort by date (newest first)
  - Add data bars for runs and wickets

### 2. Match Timeline
- **Type**: Line Chart
- **Fields**:
  - X-axis: start_date
  - Y-axis: total_runs
  - Legend: venue
- **Formatting**:
  - Smooth lines
  - Add markers
  - Tooltip showing match details
  - Y-axis range: 100-200

### 3. Venue Performance
- **Type**: Bar Chart
- **Fields**:
  - X-axis: venue
  - Y-axis: avg_total_runs
- **Formatting**:
  - Sort by average runs
  - Add data labels
  - Color gradient based on average runs

### 4. Team Performance Cards
- **Type**: Card Visuals
- **Measures**:
  - Total Matches
  - Average Runs
  - Win Rate
  - Total Boundaries
- **Formatting**:
  - Large numbers
  - Trend indicators
  - Conditional colors

## Page 2: Player Analysis

### 1. Top Batsmen
- **Type**: Bar Chart
- **Fields**:
  - X-axis: player
  - Y-axis: total_runs
- **Formatting**:
  - Top 10 players
  - Data labels
  - Color by strike rate

### 2. Strike Rate vs Average
- **Type**: Scatter Plot
- **Fields**:
  - X-axis: average
  - Y-axis: strike_rate
  - Size: total_runs
  - Legend: player
- **Formatting**:
  - Quadrant lines at average values
  - Tooltips with player stats
  - Color by boundary percentage

### 3. Partnership Heat Map
- **Type**: Matrix
- **Fields**:
  - Rows: striker
  - Columns: non_striker
  - Values: runs_off_bat
- **Formatting**:
  - Color scale
  - Conditional formatting
  - Tooltips with partnership details

## Page 3: Powerplay Analysis

### 1. Powerplay Performance
- **Type**: Bar Chart
- **Fields**:
  - X-axis: batting_team
  - Y-axis: powerplay_runs
- **Formatting**:
  - Sort by runs
  - Add target line
  - Data labels

### 2. Powerplay Impact
- **Type**: Scatter Plot
- **Fields**:
  - X-axis: powerplay_runs
  - Y-axis: match_result
  - Size: total_runs
- **Formatting**:
  - Color by result
  - Trend line
  - Tooltips with match details

## Page 4: Venue Analysis

### 1. Venue Comparison
- **Type**: Bar Chart
- **Fields**:
  - X-axis: venue
  - Y-axis: avg_total_runs
- **Formatting**:
  - Sort by average runs
  - Add target line
  - Data labels

### 2. Venue Characteristics
- **Type**: Scatter Plot
- **Fields**:
  - X-axis: boundaries
  - Y-axis: total_runs
  - Size: matches_played
- **Formatting**:
  - Color by venue
  - Trend line
  - Tooltips with venue stats

## Common Formatting Guidelines

### Color Scheme
- Primary: #1E88E5 (Blue)
- Secondary: #43A047 (Green)
- Accent: #E53935 (Red)
- Background: #F5F5F5 (Light Gray)
- Text: #212121 (Dark Gray)

### Typography
- Headers: Segoe UI, 14pt
- Body: Segoe UI, 12pt
- Numbers: Segoe UI, 11pt

### Layout
- Page margins: 20px
- Chart padding: 10px
- Grid spacing: 10px

### Interactivity
- Cross-filtering enabled
- Drill-through to detailed views
- Tooltips with additional metrics
- Bookmarks for different views

### Filters
- Date range slicer
- Team filter
- Player filter
- Venue filter
- Match type filter

## Best Practices
1. Keep visualizations simple and focused
2. Use consistent formatting across pages
3. Include clear titles and labels
4. Add context through tooltips
5. Use appropriate chart types for data
6. Implement responsive design
7. Include clear navigation
8. Add data refresh indicators 