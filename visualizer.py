"""
Visualization module for Wikipedia contribution analysis.

This module creates charts and graphs using matplotlib
to visualize user contribution patterns and statistics.
"""

import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

import config
from analyzer import ContributionStats, ContributionAnalyzer


class ContributionVisualizer:
    """
    Creates visualizations for Wikipedia contribution data.

    Generates various charts including time series, bar charts,
    pie charts, and heatmaps.
    """

    def __init__(self, stats: ContributionStats, analyzer: ContributionAnalyzer):
        """
        Initialize the visualizer.

        Args:
            stats: ContributionStats object with analysis results
            analyzer: ContributionAnalyzer for accessing raw data
        """
        self.stats = stats
        self.analyzer = analyzer
        self.colors = config.COLOR_PALETTE

        # Set matplotlib style
        plt.style.use("seaborn-v0_8-whitegrid")
        plt.rcParams["figure.dpi"] = config.FIGURE_DPI

    def _setup_output_dir(self, output_dir: str) -> Path:
        """Create output directory if it doesn't exist."""
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def plot_edits_over_time(
        self,
        output_path: str = None,
        show: bool = False
    ) -> plt.Figure:
        """
        Plot cumulative edits over time.

        Args:
            output_path: Path to save the figure
            show: Whether to display the figure

        Returns:
            matplotlib Figure object
        """
        cumulative_df = self.analyzer.get_cumulative_edits()

        if cumulative_df.empty:
            return None

        fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)

        ax.plot(
            cumulative_df["date"],
            cumulative_df["cumulative_edits"],
            color=self.colors[0],
            linewidth=2
        )

        ax.fill_between(
            cumulative_df["date"],
            cumulative_df["cumulative_edits"],
            alpha=0.3,
            color=self.colors[0]
        )

        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Cumulative Edits", fontsize=12)
        ax.set_title(
            f"Edit History for {self.stats.username}",
            fontsize=14,
            fontweight="bold"
        )

        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        if output_path:
            fig.savefig(output_path, bbox_inches="tight")
        if show:
            plt.show()

        return fig

    def plot_monthly_activity(
        self,
        output_path: str = None,
        show: bool = False
    ) -> plt.Figure:
        """
        Plot monthly edit counts as a bar chart.

        Args:
            output_path: Path to save the figure
            show: Whether to display the figure

        Returns:
            matplotlib Figure object
        """
        monthly_data = self.stats.edits_by_month

        if not monthly_data:
            return None

        fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)

        months = list(monthly_data.keys())
        counts = list(monthly_data.values())

        # Limit to last 24 months if too many
        if len(months) > 24:
            months = months[-24:]
            counts = counts[-24:]

        bars = ax.bar(range(len(months)), counts, color=self.colors[0], alpha=0.8)

        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Number of Edits", fontsize=12)
        ax.set_title(
            f"Monthly Edit Activity - {self.stats.username}",
            fontsize=14,
            fontweight="bold"
        )

        # Set x-tick labels
        step = max(1, len(months) // 12)
        ax.set_xticks(range(0, len(months), step))
        ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, ha="right")

        plt.tight_layout()

        if output_path:
            fig.savefig(output_path, bbox_inches="tight")
        if show:
            plt.show()

        return fig

    def plot_day_of_week_activity(
        self,
        output_path: str = None,
        show: bool = False
    ) -> plt.Figure:
        """
        Plot edit counts by day of week.

        Args:
            output_path: Path to save the figure
            show: Whether to display the figure

        Returns:
            matplotlib Figure object
        """
        daily_data = self.stats.edits_by_day_of_week

        if not daily_data:
            return None

        fig, ax = plt.subplots(figsize=(10, 6))

        days = list(daily_data.keys())
        counts = list(daily_data.values())

        bars = ax.bar(days, counts, color=self.colors[1], alpha=0.8)

        # Highlight weekends
        for i, bar in enumerate(bars):
            if days[i] in ["Saturday", "Sunday"]:
                bar.set_color(self.colors[3])

        ax.set_xlabel("Day of Week", fontsize=12)
        ax.set_ylabel("Number of Edits", fontsize=12)
        ax.set_title(
            f"Edits by Day of Week - {self.stats.username}",
            fontsize=14,
            fontweight="bold"
        )

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        if output_path:
            fig.savefig(output_path, bbox_inches="tight")
        if show:
            plt.show()

        return fig

    def plot_hourly_activity(
        self,
        output_path: str = None,
        show: bool = False
    ) -> plt.Figure:
        """
        Plot edit counts by hour of day.

        Args:
            output_path: Path to save the figure
            show: Whether to display the figure

        Returns:
            matplotlib Figure object
        """
        hourly_data = self.stats.edits_by_hour

        if not hourly_data:
            return None

        fig, ax = plt.subplots(figsize=(12, 6))

        hours = list(range(24))
        counts = [hourly_data.get(h, 0) for h in hours]

        ax.bar(hours, counts, color=self.colors[2], alpha=0.8)

        ax.set_xlabel("Hour of Day (UTC)", fontsize=12)
        ax.set_ylabel("Number of Edits", fontsize=12)
        ax.set_title(
            f"Edits by Hour of Day - {self.stats.username}",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xticks(hours)
        ax.set_xticklabels([f"{h:02d}:00" for h in hours], rotation=45, ha="right")

        plt.tight_layout()

        if output_path:
            fig.savefig(output_path, bbox_inches="tight")
        if show:
            plt.show()

        return fig

    def plot_top_articles(
        self,
        output_path: str = None,
        show: bool = False,
        limit: int = 15
    ) -> plt.Figure:
        """
        Plot the most edited articles as a horizontal bar chart.

        Args:
            output_path: Path to save the figure
            show: Whether to display the figure
            limit: Number of articles to show

        Returns:
            matplotlib Figure object
        """
        top_articles = self.stats.top_articles[:limit]

        if not top_articles:
            return None

        fig, ax = plt.subplots(figsize=(12, 8))

        articles = [a[0][:50] + "..." if len(a[0]) > 50 else a[0] for a in top_articles]
        counts = [a[1] for a in top_articles]

        # Reverse for horizontal bar chart (top article at top)
        articles = articles[::-1]
        counts = counts[::-1]

        colors = [self.colors[i % len(self.colors)] for i in range(len(articles))]
        ax.barh(articles, counts, color=colors, alpha=0.8)

        ax.set_xlabel("Number of Edits", fontsize=12)
        ax.set_ylabel("Article Title", fontsize=12)
        ax.set_title(
            f"Top {limit} Most Edited Articles - {self.stats.username}",
            fontsize=14,
            fontweight="bold"
        )

        plt.tight_layout()

        if output_path:
            fig.savefig(output_path, bbox_inches="tight")
        if show:
            plt.show()

        return fig

    def plot_topic_distribution(
        self,
        output_path: str = None,
        show: bool = False
    ) -> plt.Figure:
        """
        Plot topic distribution as a pie chart.

        Args:
            output_path: Path to save the figure
            show: Whether to display the figure

        Returns:
            matplotlib Figure object
        """
        topic_data = self.stats.topic_distribution

        if not topic_data:
            return None

        # Filter out zero values and limit topics
        topics = {k: v for k, v in topic_data.items() if v > 0}
        topics = dict(sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10])

        if not topics:
            return None

        fig, ax = plt.subplots(figsize=(10, 8))

        labels = list(topics.keys())
        sizes = list(topics.values())
        colors = self.colors[:len(labels)]

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
            pctdistance=0.85
        )

        # Style the text
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight("bold")

        ax.set_title(
            f"Topic Distribution - {self.stats.username}",
            fontsize=14,
            fontweight="bold"
        )

        plt.tight_layout()

        if output_path:
            fig.savefig(output_path, bbox_inches="tight")
        if show:
            plt.show()

        return fig

    def plot_edit_size_distribution(
        self,
        output_path: str = None,
        show: bool = False
    ) -> plt.Figure:
        """
        Plot distribution of edit sizes.

        Args:
            output_path: Path to save the figure
            show: Whether to display the figure

        Returns:
            matplotlib Figure object
        """
        size_data = self.stats.edit_size_distribution

        if not size_data:
            return None

        fig, ax = plt.subplots(figsize=(10, 6))

        # Order categories from large additions to large deletions
        category_order = [
            "large_addition", "medium_addition", "small_addition",
            "no_change",
            "small_deletion", "medium_deletion", "large_deletion"
        ]

        labels = [cat.replace("_", " ").title() for cat in category_order]
        sizes = [size_data.get(cat, 0) for cat in category_order]

        # Color gradient from green (additions) to red (deletions)
        colors = ["#2ca02c", "#7fc97f", "#beebb2", "#cccccc", "#f5b7b1", "#e74c3c", "#922b21"]

        bars = ax.bar(labels, sizes, color=colors, alpha=0.9)

        ax.set_xlabel("Edit Size Category", fontsize=12)
        ax.set_ylabel("Number of Edits", fontsize=12)
        ax.set_title(
            f"Edit Size Distribution - {self.stats.username}",
            fontsize=14,
            fontweight="bold"
        )

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        if output_path:
            fig.savefig(output_path, bbox_inches="tight")
        if show:
            plt.show()

        return fig

    def plot_activity_heatmap(
        self,
        output_path: str = None,
        show: bool = False
    ) -> plt.Figure:
        """
        Plot activity heatmap (day of week vs hour).

        Args:
            output_path: Path to save the figure
            show: Whether to display the figure

        Returns:
            matplotlib Figure object
        """
        heatmap_data = self.analyzer.get_activity_heatmap_data()

        if heatmap_data.empty:
            return None

        fig, ax = plt.subplots(figsize=(14, 6))

        # Create heatmap
        im = ax.imshow(heatmap_data.values, cmap="YlOrRd", aspect="auto")

        # Set ticks
        ax.set_xticks(range(24))
        ax.set_xticklabels([f"{h:02d}" for h in range(24)])
        ax.set_yticks(range(len(heatmap_data.index)))
        ax.set_yticklabels(heatmap_data.index)

        ax.set_xlabel("Hour of Day (UTC)", fontsize=12)
        ax.set_ylabel("Day of Week", fontsize=12)
        ax.set_title(
            f"Activity Heatmap - {self.stats.username}",
            fontsize=14,
            fontweight="bold"
        )

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label("Number of Edits", fontsize=10)

        plt.tight_layout()

        if output_path:
            fig.savefig(output_path, bbox_inches="tight")
        if show:
            plt.show()

        return fig

    def generate_all_visualizations(
        self,
        output_dir: str = None,
        show: bool = False
    ) -> dict[str, str]:
        """
        Generate all visualizations and save to files.

        Args:
            output_dir: Directory to save visualizations
            show: Whether to display figures

        Returns:
            Dictionary mapping chart names to file paths
        """
        if output_dir is None:
            output_dir = config.OUTPUT_DIR

        output_path = self._setup_output_dir(output_dir)
        generated_files = {}

        charts = [
            ("edits_over_time", self.plot_edits_over_time),
            ("monthly_activity", self.plot_monthly_activity),
            ("day_of_week_activity", self.plot_day_of_week_activity),
            ("hourly_activity", self.plot_hourly_activity),
            ("top_articles", self.plot_top_articles),
            ("topic_distribution", self.plot_topic_distribution),
            ("edit_size_distribution", self.plot_edit_size_distribution),
            ("activity_heatmap", self.plot_activity_heatmap),
        ]

        for chart_name, chart_func in charts:
            file_path = output_path / f"{self.stats.username}_{chart_name}.png"
            fig = chart_func(output_path=str(file_path), show=show)

            if fig:
                generated_files[chart_name] = str(file_path)
                plt.close(fig)

        return generated_files


def create_visualizations(
    stats: ContributionStats,
    analyzer: ContributionAnalyzer,
    output_dir: str = None,
    show: bool = False
) -> dict[str, str]:
    """
    Convenience function to create all visualizations.

    Args:
        stats: ContributionStats from analysis
        analyzer: ContributionAnalyzer instance
        output_dir: Directory for output files
        show: Whether to display figures

    Returns:
        Dictionary mapping chart names to file paths
    """
    visualizer = ContributionVisualizer(stats, analyzer)
    return visualizer.generate_all_visualizations(output_dir, show)
