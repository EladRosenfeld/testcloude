#!/usr/bin/env python3
"""
Wikipedia User Contribution Analyzer

A tool to fetch, analyze, and visualize Wikipedia user contributions.

Usage:
    python main.py <username> [options]

Example:
    python main.py Jimbo_Wales --output ./reports --show-charts
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import config
from wiki_api import WikipediaAPI, WikipediaAPIError
from analyzer import ContributionAnalyzer, ContributionStats
from visualizer import ContributionVisualizer


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze Wikipedia user contributions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s Jimbo_Wales
  %(prog)s Jimbo_Wales --output ./reports
  %(prog)s Jimbo_Wales --show-charts --no-report
  %(prog)s Jimbo_Wales --language de
        """
    )

    parser.add_argument(
        "username",
        help="Wikipedia username to analyze"
    )

    parser.add_argument(
        "-o", "--output",
        default=config.OUTPUT_DIR,
        help=f"Output directory for reports and charts (default: {config.OUTPUT_DIR})"
    )

    parser.add_argument(
        "-l", "--language",
        default="en",
        help="Wikipedia language code (default: en)"
    )

    parser.add_argument(
        "--show-charts",
        action="store_true",
        help="Display charts interactively"
    )

    parser.add_argument(
        "--no-charts",
        action="store_true",
        help="Skip generating chart images"
    )

    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip generating text report"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Export statistics as JSON"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output"
    )

    return parser.parse_args()


def print_summary(stats: ContributionStats) -> None:
    """Print a summary of the analysis to console."""
    print("\n" + "=" * 60)
    print(f"  CONTRIBUTION ANALYSIS: {stats.username}")
    print("=" * 60)

    print(f"\n📊 Overview")
    print(f"   Total Edits: {stats.total_edits:,}")
    print(f"   Unique Articles: {stats.unique_articles:,}")
    print(f"   Active Period: {stats.active_days:,} days")

    if stats.first_edit and stats.last_edit:
        print(f"   First Edit: {stats.first_edit.strftime('%Y-%m-%d')}")
        print(f"   Last Edit: {stats.last_edit.strftime('%Y-%m-%d')}")

    print(f"\n📝 Edit Statistics")
    print(f"   Minor Edits: {stats.minor_edits:,} ({100*stats.minor_edits/max(stats.total_edits,1):.1f}%)")
    print(f"   New Pages Created: {stats.new_pages_created:,}")
    print(f"   Avg Edits/Day: {stats.avg_edits_per_day:.2f}")

    print(f"\n📏 Size Statistics")
    print(f"   Total Additions: +{stats.total_additions:,} bytes")
    print(f"   Total Deletions: -{stats.total_deletions:,} bytes")
    print(f"   Net Contribution: {stats.net_contribution:+,} bytes")

    if stats.top_articles:
        print(f"\n🏆 Top 5 Most Edited Articles")
        for i, (title, count) in enumerate(stats.top_articles[:5], 1):
            display_title = title[:45] + "..." if len(title) > 45 else title
            print(f"   {i}. {display_title} ({count} edits)")

    if stats.topic_distribution:
        print(f"\n📚 Top Topics")
        sorted_topics = sorted(
            stats.topic_distribution.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for topic, count in sorted_topics:
            if count > 0:
                pct = 100 * count / stats.total_edits
                print(f"   • {topic.title()}: {count:,} edits ({pct:.1f}%)")

    print("\n" + "=" * 60)


def generate_report(stats: ContributionStats, output_dir: str) -> str:
    """
    Generate a detailed text report.

    Args:
        stats: ContributionStats object
        output_dir: Directory to save the report

    Returns:
        Path to the generated report
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    report_path = Path(output_dir) / f"{stats.username}_report.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write(f"WIKIPEDIA CONTRIBUTION ANALYSIS REPORT\n")
        f.write(f"User: {stats.username}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        f.write("OVERVIEW\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Edits: {stats.total_edits:,}\n")
        f.write(f"Unique Articles Edited: {stats.unique_articles:,}\n")
        f.write(f"Active Period: {stats.active_days:,} days\n")
        if stats.first_edit:
            f.write(f"First Edit: {stats.first_edit.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        if stats.last_edit:
            f.write(f"Last Edit: {stats.last_edit.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write(f"Average Edits per Day: {stats.avg_edits_per_day:.2f}\n\n")

        f.write("EDIT STATISTICS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Minor Edits: {stats.minor_edits:,} ({100*stats.minor_edits/max(stats.total_edits,1):.1f}%)\n")
        f.write(f"New Pages Created: {stats.new_pages_created:,}\n")
        f.write(f"Total Additions: +{stats.total_additions:,} bytes\n")
        f.write(f"Total Deletions: -{stats.total_deletions:,} bytes\n")
        f.write(f"Net Contribution: {stats.net_contribution:+,} bytes\n\n")

        f.write("TOP 20 MOST EDITED ARTICLES\n")
        f.write("-" * 40 + "\n")
        for i, (title, count) in enumerate(stats.top_articles[:20], 1):
            f.write(f"{i:2}. {title} ({count} edits)\n")
        f.write("\n")

        f.write("TOPIC DISTRIBUTION\n")
        f.write("-" * 40 + "\n")
        sorted_topics = sorted(
            stats.topic_distribution.items(),
            key=lambda x: x[1],
            reverse=True
        )
        for topic, count in sorted_topics:
            if count > 0:
                pct = 100 * count / stats.total_edits
                f.write(f"{topic.title():20} {count:8,} edits ({pct:5.1f}%)\n")
        f.write("\n")

        f.write("ACTIVITY BY DAY OF WEEK\n")
        f.write("-" * 40 + "\n")
        for day, count in stats.edits_by_day_of_week.items():
            bar = "█" * (count * 40 // max(stats.edits_by_day_of_week.values(), 1))
            f.write(f"{day:10} {count:6,} {bar}\n")
        f.write("\n")

        f.write("ACTIVITY BY HOUR (UTC)\n")
        f.write("-" * 40 + "\n")
        max_hourly = max(stats.edits_by_hour.values()) if stats.edits_by_hour else 1
        for hour in range(24):
            count = stats.edits_by_hour.get(hour, 0)
            bar = "█" * (count * 30 // max_hourly) if max_hourly > 0 else ""
            f.write(f"{hour:02d}:00  {count:6,} {bar}\n")
        f.write("\n")

        f.write("EDIT SIZE DISTRIBUTION\n")
        f.write("-" * 40 + "\n")
        for category, count in stats.edit_size_distribution.items():
            label = category.replace("_", " ").title()
            pct = 100 * count / max(stats.total_edits, 1)
            f.write(f"{label:20} {count:8,} ({pct:5.1f}%)\n")
        f.write("\n")

        f.write("=" * 70 + "\n")
        f.write("Report generated by Wikipedia User Contribution Analyzer\n")
        f.write("=" * 70 + "\n")

    return str(report_path)


def export_json(stats: ContributionStats, output_dir: str) -> str:
    """
    Export statistics as JSON.

    Args:
        stats: ContributionStats object
        output_dir: Directory to save the JSON file

    Returns:
        Path to the generated JSON file
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    json_path = Path(output_dir) / f"{stats.username}_stats.json"

    data = {
        "username": stats.username,
        "generated_at": datetime.now().isoformat(),
        "overview": {
            "total_edits": stats.total_edits,
            "unique_articles": stats.unique_articles,
            "active_days": stats.active_days,
            "first_edit": stats.first_edit.isoformat() if stats.first_edit else None,
            "last_edit": stats.last_edit.isoformat() if stats.last_edit else None,
            "avg_edits_per_day": round(stats.avg_edits_per_day, 2),
        },
        "edit_statistics": {
            "minor_edits": stats.minor_edits,
            "new_pages_created": stats.new_pages_created,
            "total_additions_bytes": stats.total_additions,
            "total_deletions_bytes": stats.total_deletions,
            "net_contribution_bytes": stats.net_contribution,
        },
        "top_articles": [
            {"title": title, "edit_count": count}
            for title, count in stats.top_articles
        ],
        "topic_distribution": stats.topic_distribution,
        "edits_by_month": stats.edits_by_month,
        "edits_by_day_of_week": stats.edits_by_day_of_week,
        "edits_by_hour": stats.edits_by_hour,
        "edit_size_distribution": stats.edit_size_distribution,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return str(json_path)


def main() -> int:
    """Main entry point for the application."""
    args = parse_arguments()

    # Initialize API client
    api = WikipediaAPI(language=args.language)

    # Check if user exists
    if not args.quiet:
        print(f"\n🔍 Checking user: {args.username}")

    try:
        if not api.check_user_exists(args.username):
            print(f"❌ Error: User '{args.username}' not found on {args.language}.wikipedia.org")
            return 1
    except WikipediaAPIError as e:
        print(f"❌ API Error: {e}")
        return 1

    # Fetch contributions
    if not args.quiet:
        print(f"📥 Fetching contributions...")

    try:
        contributions = api.fetch_contributions(
            args.username,
            show_progress=not args.quiet
        )
    except WikipediaAPIError as e:
        print(f"❌ Error fetching contributions: {e}")
        return 1

    if not contributions:
        print(f"ℹ️  User '{args.username}' has no contributions.")
        return 0

    # Analyze contributions
    if not args.quiet:
        print(f"📊 Analyzing {len(contributions):,} contributions...")

    analyzer = ContributionAnalyzer(contributions, args.username)
    stats = analyzer.analyze()

    # Print summary to console
    if not args.quiet:
        print_summary(stats)

    # Generate outputs
    generated_files = []

    # Generate text report
    if not args.no_report:
        report_path = generate_report(stats, args.output)
        generated_files.append(("Report", report_path))
        if not args.quiet:
            print(f"📄 Report saved: {report_path}")

    # Export JSON if requested
    if args.json:
        json_path = export_json(stats, args.output)
        generated_files.append(("JSON", json_path))
        if not args.quiet:
            print(f"📋 JSON exported: {json_path}")

    # Generate visualizations
    if not args.no_charts:
        if not args.quiet:
            print(f"📈 Generating visualizations...")

        visualizer = ContributionVisualizer(stats, analyzer)
        chart_files = visualizer.generate_all_visualizations(
            output_dir=args.output,
            show=args.show_charts
        )

        for chart_name, chart_path in chart_files.items():
            generated_files.append((chart_name, chart_path))

        if not args.quiet:
            print(f"   Generated {len(chart_files)} charts in {args.output}/")

    # Summary
    if not args.quiet and generated_files:
        print(f"\n✅ Analysis complete! Generated {len(generated_files)} files.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
