# SA20 Cricket Data Analysis

This project analyzes cricket data from the SA20 league, providing insights into player performance, team statistics, and match dynamics.

## Features

- Powerplay Analysis (first 6 overs)
- Player Partnership Analysis
- Venue Analysis
- Match Momentum Tracking
- Player Form Analysis
- Head-to-Head Statistics

## Project Structure

```
sa20_cricket_data/
├── src/
│   └── analysis/
│       ├── cricket_analysis.py    # Core analysis functionality
│       └── run_sa20_analysis.py   # Script to run analysis and save results
├── analysis_results/             # Generated analysis results
├── all_matches.csv              # Raw match data
└── README.md
```

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sa20_cricket_data.git
cd sa20_cricket_data
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

To run the analysis:

```bash
python src/analysis/run_sa20_analysis.py
```

This will:
1. Process the cricket data
2. Generate various analyses
3. Save results in the `analysis_results` directory
4. Create visualizations
5. Generate a summary statistics file

## Output

The analysis generates several output files in the `analysis_results` directory:
- `powerplay_batting.csv`: Batting statistics during powerplay overs
- `powerplay_bowling.csv`: Bowling statistics during powerplay overs
- `partnerships.csv`: Partnership analysis
- `venue_stats.csv`: Venue-specific statistics
- `powerplay_strike_rate_dist.png`: Visualization of powerplay strike rates
- `venue_comparison.png`: Comparison of venues
- `summary_stats.json`: Overall summary statistics

## Data Source

The data is sourced from the SA20 league matches and includes detailed ball-by-ball information.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 