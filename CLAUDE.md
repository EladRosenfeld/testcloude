# CLAUDE.md - AI Assistant Guidelines

> This file provides context and guidelines for AI assistants working with this repository.

## Project Overview

**Repository**: testcloude
**Owner**: EladRosenfeld
**Project**: Wikipedia User Contribution Analyzer
**Language**: Python 3.10+

A tool to fetch, analyze, and visualize Wikipedia user contributions. It retrieves edit history via the Wikipedia API, performs comprehensive analysis, and generates visualizations and reports.

---

## Repository Structure

```
testcloude/
├── main.py             # CLI entry point and orchestration
├── wiki_api.py         # Wikipedia API client
├── analyzer.py         # Data analysis and statistics
├── visualizer.py       # Chart and graph generation
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── README.md           # User documentation
├── CLAUDE.md           # AI assistant guidelines (this file)
├── .gitignore          # Git ignore patterns
└── output/             # Generated reports and charts (gitignored)
```

---

## Module Overview

### main.py
- Entry point with CLI argument parsing
- Orchestrates API calls, analysis, and visualization
- Generates text reports and JSON exports
- Key functions: `main()`, `print_summary()`, `generate_report()`, `export_json()`

### wiki_api.py
- `WikipediaAPI` class for API interactions
- Handles pagination, rate limiting, retries
- Key methods: `fetch_contributions()`, `check_user_exists()`, `get_user_info()`

### analyzer.py
- `ContributionAnalyzer` class for data processing
- `ContributionStats` dataclass for results
- Temporal analysis, topic categorization, edit size stats
- Uses pandas for data manipulation

### visualizer.py
- `ContributionVisualizer` class for matplotlib charts
- Generates 8 different chart types
- Supports saving to files and interactive display

### config.py
- API endpoints and request parameters
- Rate limiting settings
- Visualization configuration
- Topic categorization keywords

---

## Development Guidelines

### Git Workflow

1. **Branch Naming**:
   - Features: `feature/<description>`
   - Fixes: `fix/<description>`
   - Claude sessions: `claude/<session-id>`

2. **Commit Messages**: Follow conventional commits
   ```
   type(scope): description
   ```
   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings for public functions and classes
- Keep functions focused and single-purpose
- Prefer descriptive names over comments

### Testing

- Test new API interactions with mock responses
- Verify analysis logic with known data sets
- Ensure visualizations render without errors

---

## Commands Reference

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run analyzer
python main.py <username>

# Run with options
python main.py <username> --output ./reports --show-charts

# Quick test (quiet mode, no charts)
python main.py <username> -q --no-charts
```

---

## AI Assistant Instructions

### When Working on This Repository

1. **Read Before Editing**: Always read files before modifying them
2. **Understand the Pipeline**: API → Analysis → Visualization → Export
3. **Follow Conventions**: Match existing code patterns
4. **Minimal Changes**: Only change what's necessary
5. **Test Changes**: Run the tool with a real username to verify

### Key Patterns to Follow

- Use dataclasses for structured data (`ContributionStats`)
- Use type hints consistently
- Handle API errors with custom exceptions (`WikipediaAPIError`)
- Respect rate limiting when making API calls
- Use pandas for data manipulation in analyzer.py

### Do's

- Add proper error handling for API failures
- Use existing config values from `config.py`
- Keep visualization functions modular
- Update docstrings when modifying functions

### Don'ts

- Don't hardcode API endpoints (use config.py)
- Don't remove rate limiting delays
- Don't add blocking operations without timeouts
- Don't commit API keys or credentials

---

## Configuration Files

| File | Purpose |
|------|---------|
| `config.py` | API settings, visualization config, topic keywords |
| `requirements.txt` | Python package dependencies |
| `.gitignore` | Excludes output files, venv, cache |

---

## Architecture Notes

### Data Flow

```
Wikipedia API → raw JSON contributions
     ↓
ContributionAnalyzer → pandas DataFrame → ContributionStats
     ↓
ContributionVisualizer → matplotlib figures → PNG files
     ↓
main.py → text report / JSON export
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP client for Wikipedia API |
| `pandas` | Data analysis and manipulation |
| `matplotlib` | Chart and graph generation |
| `python-dateutil` | Timestamp parsing |
| `tqdm` | Progress bar display |

---

## Troubleshooting

### Common Issues

1. **API rate limiting errors**
   - Increase `REQUEST_DELAY` in config.py
   - Add exponential backoff for retries

2. **User not found**
   - Check username spelling and case sensitivity
   - Verify language code matches user's Wikipedia

3. **No contributions fetched**
   - User may have 0 edits
   - API pagination might have failed

4. **Matplotlib display issues**
   - Use `--no-charts` flag to skip visualization
   - Check matplotlib backend configuration

---

## Changelog

| Date | Changes |
|------|---------|
| 2026-01-29 | Initial CLAUDE.md created |
| 2026-01-29 | Added Wikipedia User Contribution Analyzer project |

---

*Last updated: 2026-01-29*
