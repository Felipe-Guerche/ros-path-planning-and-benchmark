#!/usr/bin/env python3
"""
Benchmark Results Analyzer
- Merges multiple CSV files from parallel Docker containers.
- Runs Shapiro-Wilk normality tests.
- Runs Kruskal-Wallis + pairwise Mann-Whitney U tests.
- Outputs results to console and optionally to a report file.
"""

import os
import sys
import glob
import argparse

import pandas as pd
from scipy import stats


def find_and_merge_csvs(results_dir):
    """Find all battery_summary_*.csv files and merge into one DataFrame."""
    pattern = os.path.join(results_dir, "battery_summary_*.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No summary files found in: {results_dir}")
        sys.exit(1)

    print(f"Found {len(files)} summary file(s):")
    for f in files:
        print(f"  - {os.path.basename(f)}")

    dfs = [pd.read_csv(f) for f in files]
    merged = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal rows after merge: {len(merged)}")
    return merged


def run_normality_tests(groups, metric_name):
    """Run Shapiro-Wilk test on each group."""
    print(f"\n=== Shapiro-Wilk Normality Test ({metric_name}) ===")
    print(f"H0: Data is normally distributed (p > 0.05)\n")
    results = {}
    for name, values in groups.items():
        if len(values) >= 3:
            stat, p = stats.shapiro(values)
            is_normal = p > 0.05
            results[name] = {"W": stat, "p": p, "normal": is_normal}
            tag = "Normal" if is_normal else "NOT Normal"
            print(f"  {name:25s} | W={stat:.4f}  p={p:.6f}  => {tag}")
        else:
            print(f"  {name:25s} | Too few samples ({len(values)})")
    return results


def run_kruskal_wallis(groups, metric_name):
    """Run Kruskal-Wallis H-test and, if significant, pairwise Mann-Whitney U."""
    print(f"\n=== Kruskal-Wallis H-Test ({metric_name}) ===")
    if len(groups) < 2:
        print("  Need at least 2 groups to compare.")
        return

    stat, p = stats.kruskal(*groups.values())
    print(f"  H={stat:.4f}  p={p:.6f}")

    if p < 0.05:
        print("  => Statistically significant difference between groups.\n")
        print(f"  --- Pairwise Mann-Whitney U ({metric_name}) ---")
        names = list(groups.keys())
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                u_stat, u_p = stats.mannwhitneyu(
                    groups[names[i]], groups[names[j]], alternative="two-sided"
                )
                tag = "DIFFERENT" if u_p < 0.05 else "similar"
                print(f"  {names[i]:20s} vs {names[j]:20s} | U={u_stat:.1f}  p={u_p:.6f}  => {tag}")
    else:
        print("  => No statistically significant difference between groups.")


def analyze(df, group_col="GlobalPlanner", metrics=None):
    """Run full statistical analysis on the DataFrame."""
    if metrics is None:
        metrics = ["Time(s)", "Distance(m)", "CPU(%)", "Memory(MiB)"]

    # Filter successful runs
    if "Status" in df.columns:
        successful = df[df["Status"] == "Success"]
        print(f"\nSuccessful runs: {len(successful)} / {len(df)}")
    else:
        successful = df
        print(f"\nTotal runs: {len(df)} (no Status column, using all)")

    if successful.empty:
        print("No successful runs to analyze.")
        return

    for metric in metrics:
        if metric not in successful.columns:
            print(f"\nSkipping metric '{metric}' (not found in CSV)")
            continue

        print(f"\n{'='*60}")
        print(f"  METRIC: {metric}")
        print(f"{'='*60}")

        # Descriptive stats
        print(f"\n--- Descriptive Statistics ---")
        desc = successful.groupby(group_col)[metric].describe()
        print(desc.to_string())

        # Build groups
        groups = {}
        for name, group in successful.groupby(group_col):
            vals = group[metric].dropna().values
            if len(vals) >= 3:
                groups[name] = vals

        if len(groups) < 2:
            print(f"\n  Not enough groups with >= 3 samples for statistical tests.")
            continue

        run_normality_tests(groups, metric)
        run_kruskal_wallis(groups, metric)


def main():
    parser = argparse.ArgumentParser(description="Analyze Benchmark Results")
    parser.add_argument(
        "--results_dir",
        type=str,
        default=None,
        help="Directory containing battery_summary_*.csv files",
    )
    parser.add_argument(
        "--summary_file",
        type=str,
        default=None,
        help="Path to a single summary CSV (overrides --results_dir)",
    )
    parser.add_argument(
        "--group_by",
        type=str,
        default="GlobalPlanner",
        help="Column to group by for comparison (default: GlobalPlanner)",
    )
    args = parser.parse_args()

    if args.summary_file:
        print(f"Analyzing single file: {args.summary_file}")
        df = pd.read_csv(args.summary_file)
    else:
        results_dir = args.results_dir or os.path.join(
            os.path.dirname(__file__), "..", "src", "plannie-main", "results"
        )
        df = find_and_merge_csvs(results_dir)

    # Save merged CSV for reproducibility
    if args.results_dir:
        merged_path = os.path.join(args.results_dir, "merged_results.csv")
        df.to_csv(merged_path, index=False)
        print(f"\nMerged CSV saved to: {merged_path}")

    analyze(df, group_col=args.group_by)


if __name__ == "__main__":
    main()
