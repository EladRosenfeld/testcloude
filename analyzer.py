"""
Data analysis module for Wikipedia contributions.

This module provides functions to analyze user contributions,
including temporal patterns, topic categorization, and statistics.
"""

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil import parser as date_parser

import config


@dataclass
class ContributionStats:
    """Container for contribution statistics."""

    username: str
    total_edits: int = 0
    total_additions: int = 0
    total_deletions: int = 0
    unique_articles: int = 0
    first_edit: Optional[datetime] = None
    last_edit: Optional[datetime] = None
    minor_edits: int = 0
    new_pages_created: int = 0

    # Detailed statistics
    edits_by_month: dict = field(default_factory=dict)
    edits_by_day_of_week: dict = field(default_factory=dict)
    edits_by_hour: dict = field(default_factory=dict)
    top_articles: list = field(default_factory=list)
    topic_distribution: dict = field(default_factory=dict)
    edit_size_distribution: dict = field(default_factory=dict)

    @property
    def active_days(self) -> int:
        """Calculate number of days between first and last edit."""
        if self.first_edit and self.last_edit:
            return (self.last_edit - self.first_edit).days + 1
        return 0

    @property
    def avg_edits_per_day(self) -> float:
        """Calculate average edits per active day."""
        if self.active_days > 0:
            return self.total_edits / self.active_days
        return 0.0

    @property
    def net_contribution(self) -> int:
        """Calculate net bytes contributed (additions - deletions)."""
        return self.total_additions - self.total_deletions


class ContributionAnalyzer:
    """
    Analyzer for Wikipedia user contributions.

    Processes raw contribution data and generates comprehensive statistics.
    """

    def __init__(self, contributions: list[dict], username: str):
        """
        Initialize the analyzer with contribution data.

        Args:
            contributions: List of contribution dictionaries from API
            username: The Wikipedia username
        """
        self.raw_contributions = contributions
        self.username = username
        self.df = self._create_dataframe()

    def _create_dataframe(self) -> pd.DataFrame:
        """
        Convert raw contributions to a pandas DataFrame.

        Returns:
            DataFrame with processed contribution data
        """
        if not self.raw_contributions:
            return pd.DataFrame()

        records = []
        for contrib in self.raw_contributions:
            timestamp = date_parser.parse(contrib.get("timestamp", ""))

            records.append({
                "revid": contrib.get("revid"),
                "pageid": contrib.get("pageid"),
                "title": contrib.get("title", ""),
                "timestamp": timestamp,
                "comment": contrib.get("comment", ""),
                "size": contrib.get("size", 0),
                "sizediff": contrib.get("sizediff", 0),
                "minor": "minor" in contrib,
                "new": "new" in contrib,
                "tags": contrib.get("tags", []),
            })

        df = pd.DataFrame(records)

        # Add derived columns
        if not df.empty:
            df["year"] = df["timestamp"].dt.year
            df["month"] = df["timestamp"].dt.to_period("M")
            df["day_of_week"] = df["timestamp"].dt.day_name()
            df["hour"] = df["timestamp"].dt.hour
            df["date"] = df["timestamp"].dt.date

        return df

    def analyze(self) -> ContributionStats:
        """
        Perform full analysis of contributions.

        Returns:
            ContributionStats object with all statistics
        """
        stats = ContributionStats(username=self.username)

        if self.df.empty:
            return stats

        # Basic statistics
        stats.total_edits = len(self.df)
        stats.unique_articles = self.df["title"].nunique()
        stats.first_edit = self.df["timestamp"].min().to_pydatetime()
        stats.last_edit = self.df["timestamp"].max().to_pydatetime()
        stats.minor_edits = self.df["minor"].sum()
        stats.new_pages_created = self.df["new"].sum()

        # Size statistics
        positive_diffs = self.df[self.df["sizediff"] > 0]["sizediff"].sum()
        negative_diffs = abs(self.df[self.df["sizediff"] < 0]["sizediff"].sum())
        stats.total_additions = int(positive_diffs)
        stats.total_deletions = int(negative_diffs)

        # Temporal statistics
        stats.edits_by_month = self._analyze_edits_by_month()
        stats.edits_by_day_of_week = self._analyze_edits_by_day_of_week()
        stats.edits_by_hour = self._analyze_edits_by_hour()

        # Article statistics
        stats.top_articles = self._analyze_top_articles()

        # Topic analysis
        stats.topic_distribution = self._analyze_topics()

        # Edit size distribution
        stats.edit_size_distribution = self._analyze_edit_sizes()

        return stats

    def _analyze_edits_by_month(self) -> dict[str, int]:
        """
        Analyze edit counts by month.

        Returns:
            Dictionary mapping month strings to edit counts
        """
        monthly = self.df.groupby("month").size()
        return {str(k): int(v) for k, v in monthly.items()}

    def _analyze_edits_by_day_of_week(self) -> dict[str, int]:
        """
        Analyze edit counts by day of week.

        Returns:
            Dictionary mapping day names to edit counts
        """
        # Ensure correct ordering
        day_order = [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ]
        daily = self.df.groupby("day_of_week").size()
        return {day: int(daily.get(day, 0)) for day in day_order}

    def _analyze_edits_by_hour(self) -> dict[int, int]:
        """
        Analyze edit counts by hour of day.

        Returns:
            Dictionary mapping hour (0-23) to edit counts
        """
        hourly = self.df.groupby("hour").size()
        return {hour: int(hourly.get(hour, 0)) for hour in range(24)}

    def _analyze_top_articles(self, limit: int = None) -> list[tuple[str, int]]:
        """
        Find the most frequently edited articles.

        Args:
            limit: Maximum number of articles to return

        Returns:
            List of (article_title, edit_count) tuples
        """
        if limit is None:
            limit = config.TOP_ARTICLES_LIMIT

        article_counts = self.df["title"].value_counts().head(limit)
        return [(title, int(count)) for title, count in article_counts.items()]

    def _analyze_topics(self) -> dict[str, int]:
        """
        Categorize edits by topic based on article titles.

        Uses keyword matching to assign topics to articles.

        Returns:
            Dictionary mapping topic names to edit counts
        """
        topic_counts = Counter()
        titles_lower = self.df["title"].str.lower()

        for topic, keywords in config.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                matches = titles_lower.str.contains(keyword, na=False)
                topic_counts[topic] += matches.sum()

        # Articles that don't match any category
        matched = set()
        for topic, keywords in config.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                matched.update(
                    self.df[titles_lower.str.contains(keyword, na=False)].index
                )
        topic_counts["other"] = len(self.df) - len(matched)

        return dict(topic_counts.most_common())

    def _analyze_edit_sizes(self) -> dict[str, int]:
        """
        Categorize edits by size change.

        Returns:
            Dictionary mapping size categories to counts
        """
        size_diffs = self.df["sizediff"]

        categories = {
            "large_addition": (size_diffs > 1000).sum(),
            "medium_addition": ((size_diffs > 100) & (size_diffs <= 1000)).sum(),
            "small_addition": ((size_diffs > 0) & (size_diffs <= 100)).sum(),
            "no_change": (size_diffs == 0).sum(),
            "small_deletion": ((size_diffs < 0) & (size_diffs >= -100)).sum(),
            "medium_deletion": ((size_diffs < -100) & (size_diffs >= -1000)).sum(),
            "large_deletion": (size_diffs < -1000).sum(),
        }

        return {k: int(v) for k, v in categories.items()}

    def get_activity_heatmap_data(self) -> pd.DataFrame:
        """
        Generate data for activity heatmap (day of week vs hour).

        Returns:
            DataFrame with day of week as index, hours as columns
        """
        if self.df.empty:
            return pd.DataFrame()

        pivot = self.df.pivot_table(
            index="day_of_week",
            columns="hour",
            aggfunc="size",
            fill_value=0
        )

        # Reorder days
        day_order = [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ]
        pivot = pivot.reindex(day_order)

        return pivot

    def get_cumulative_edits(self) -> pd.DataFrame:
        """
        Calculate cumulative edit count over time.

        Returns:
            DataFrame with date index and cumulative edit count
        """
        if self.df.empty:
            return pd.DataFrame()

        daily_edits = self.df.groupby("date").size()
        cumulative = daily_edits.cumsum()

        return pd.DataFrame({
            "date": cumulative.index,
            "cumulative_edits": cumulative.values
        })

    def get_monthly_summary(self) -> pd.DataFrame:
        """
        Generate monthly summary statistics.

        Returns:
            DataFrame with monthly statistics
        """
        if self.df.empty:
            return pd.DataFrame()

        monthly = self.df.groupby("month").agg({
            "revid": "count",
            "sizediff": ["sum", "mean"],
            "title": "nunique",
            "minor": "sum",
            "new": "sum"
        })

        monthly.columns = [
            "total_edits", "total_size_change", "avg_size_change",
            "unique_articles", "minor_edits", "new_pages"
        ]

        return monthly.reset_index()


def analyze_contributions(contributions: list[dict], username: str) -> ContributionStats:
    """
    Convenience function to analyze contributions.

    Args:
        contributions: List of contribution dictionaries
        username: Wikipedia username

    Returns:
        ContributionStats object with analysis results
    """
    analyzer = ContributionAnalyzer(contributions, username)
    return analyzer.analyze()
