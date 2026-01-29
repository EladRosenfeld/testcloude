"""
Configuration settings for Wikipedia User Contribution Analyzer.

This module contains API endpoints, request parameters, and application settings.
"""

# Wikipedia API Configuration
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Default request parameters
DEFAULT_PARAMS = {
    "action": "query",
    "format": "json",
    "formatversion": "2",
}

# User contributions query parameters
USER_CONTRIBUTIONS_PARAMS = {
    "list": "usercontribs",
    "uclimit": "500",  # Max allowed per request
    "ucprop": "ids|title|timestamp|comment|size|sizediff|flags|tags",
}

# API request settings
REQUEST_TIMEOUT = 30  # seconds
REQUEST_DELAY = 0.5  # seconds between requests (be nice to Wikipedia servers)
MAX_RETRIES = 3

# User-Agent (required by Wikipedia API)
# See: https://meta.wikimedia.org/wiki/User-Agent_policy
USER_AGENT = "WikipediaContributionAnalyzer/1.0 (https://github.com/example/wiki-analyzer; contact@example.com)"

# Output settings
OUTPUT_DIR = "output"
REPORT_FILENAME = "contribution_report"

# Visualization settings
FIGURE_DPI = 150
FIGURE_SIZE = (12, 8)
COLOR_PALETTE = [
    "#1f77b4",  # Blue
    "#ff7f0e",  # Orange
    "#2ca02c",  # Green
    "#d62728",  # Red
    "#9467bd",  # Purple
    "#8c564b",  # Brown
    "#e377c2",  # Pink
    "#7f7f7f",  # Gray
    "#bcbd22",  # Yellow-green
    "#17becf",  # Cyan
]

# Analysis settings
TOP_ARTICLES_LIMIT = 20
TOP_CATEGORIES_LIMIT = 15
TIME_BINS = 24  # For hourly activity analysis

# Category detection keywords
# Maps keywords to category names for topic classification
CATEGORY_KEYWORDS = {
    "science": ["science", "physics", "chemistry", "biology", "astronomy", "mathematics"],
    "technology": ["technology", "computer", "software", "programming", "internet", "digital"],
    "history": ["history", "war", "ancient", "medieval", "century", "historical"],
    "geography": ["geography", "country", "city", "river", "mountain", "island"],
    "politics": ["politics", "government", "election", "president", "minister", "parliament"],
    "sports": ["sport", "football", "basketball", "olympics", "athlete", "championship"],
    "arts": ["art", "music", "film", "movie", "painting", "sculpture", "theatre"],
    "literature": ["literature", "novel", "author", "poetry", "writer", "book"],
    "biography": ["biography", "born", "died", "life", "career"],
    "entertainment": ["entertainment", "television", "celebrity", "actor", "singer"],
}
