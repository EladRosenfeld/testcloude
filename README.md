# Wikipedia User Contribution Analyzer

A Python tool to fetch, analyze, and visualize Wikipedia user contributions. Generate comprehensive statistics and visualizations about any Wikipedia editor's activity.

## Features

- **Fetch Contributions**: Retrieve all edits made by a Wikipedia user via the official API
- **Comprehensive Analysis**:
  - Total edits and unique articles
  - Edit timeline and activity patterns
  - Most edited articles
  - Topic categorization
  - Edit size analysis (additions/deletions)
- **Visualizations**:
  - Cumulative edits over time
  - Monthly activity bar charts
  - Day-of-week distribution
  - Hourly activity patterns
  - Activity heatmaps
  - Topic distribution pie charts
  - Edit size distribution
- **Export Options**:
  - Detailed text reports
  - JSON data export
  - PNG chart images

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/EladRosenfeld/testcloude.git
   cd testcloude
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Analyze a Wikipedia user's contributions:

```bash
python main.py <username>
```

Example:
```bash
python main.py Jimbo_Wales
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `username` | Wikipedia username to analyze (required) |
| `-o, --output DIR` | Output directory for reports and charts (default: `output/`) |
| `-l, --language CODE` | Wikipedia language code (default: `en`) |
| `--show-charts` | Display charts interactively |
| `--no-charts` | Skip generating chart images |
| `--no-report` | Skip generating text report |
| `--json` | Export statistics as JSON |
| `-q, --quiet` | Suppress progress output |

### Examples

```bash
# Basic analysis with all outputs
python main.py Jimbo_Wales

# Analyze German Wikipedia user
python main.py Example_User --language de

# Custom output directory
python main.py Jimbo_Wales --output ./reports

# Display charts interactively
python main.py Jimbo_Wales --show-charts

# Export only JSON (no charts or report)
python main.py Jimbo_Wales --json --no-charts --no-report

# Quiet mode (minimal output)
python main.py Jimbo_Wales -q
```

## Output Files

After analysis, the following files are generated in the output directory:

| File | Description |
|------|-------------|
| `{username}_report.txt` | Detailed text report |
| `{username}_stats.json` | JSON statistics (if `--json` flag used) |
| `{username}_edits_over_time.png` | Cumulative edit timeline |
| `{username}_monthly_activity.png` | Monthly edit counts |
| `{username}_day_of_week_activity.png` | Edits by day of week |
| `{username}_hourly_activity.png` | Edits by hour (UTC) |
| `{username}_top_articles.png` | Most edited articles |
| `{username}_topic_distribution.png` | Topic category breakdown |
| `{username}_edit_size_distribution.png` | Edit size categories |
| `{username}_activity_heatmap.png` | Day/hour activity heatmap |

## Project Structure

```
testcloude/
├── main.py           # Main entry point and CLI
├── wiki_api.py       # Wikipedia API interactions
├── analyzer.py       # Data analysis logic
├── visualizer.py     # Chart generation
├── config.py         # Configuration settings
├── requirements.txt  # Python dependencies
├── README.md         # This file
├── CLAUDE.md         # AI assistant guidelines
└── .gitignore        # Git ignore patterns
```

## Module Documentation

### config.py

Configuration settings including:
- Wikipedia API endpoints and parameters
- Request timeout and rate limiting
- Visualization settings (colors, figure size)
- Topic categorization keywords

### wiki_api.py

`WikipediaAPI` class for interacting with the Wikipedia API:
- `check_user_exists(username)` - Verify user exists
- `get_user_info(username)` - Get user details
- `fetch_contributions(username)` - Get all user contributions
- `get_page_categories(titles)` - Get categories for pages

### analyzer.py

`ContributionAnalyzer` class for data analysis:
- Creates pandas DataFrame from raw contributions
- Calculates temporal statistics (by month, day, hour)
- Identifies top edited articles
- Categorizes edits by topic
- Analyzes edit sizes

`ContributionStats` dataclass containing all analysis results.

### visualizer.py

`ContributionVisualizer` class for generating charts:
- Timeline plots
- Bar charts
- Pie charts
- Heatmaps

## Configuration

Edit `config.py` to customize:

```python
# Adjust API rate limiting
REQUEST_DELAY = 0.5  # seconds between requests

# Change visualization settings
FIGURE_DPI = 150
FIGURE_SIZE = (12, 8)

# Modify topic keywords for categorization
CATEGORY_KEYWORDS = {
    "science": ["science", "physics", ...],
    ...
}
```

## API Rate Limiting

This tool respects Wikipedia's API guidelines:
- Includes a proper User-Agent header
- Implements delays between requests
- Uses pagination to handle large contribution lists

## Limitations

- Topic categorization uses keyword matching and may not be 100% accurate
- Timestamps are in UTC
- Very active users (100k+ edits) may take several minutes to fetch

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source. See LICENSE file for details.

## Acknowledgments

- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) for providing access to contribution data
- [Matplotlib](https://matplotlib.org/) for visualization capabilities
- [Pandas](https://pandas.pydata.org/) for data analysis
