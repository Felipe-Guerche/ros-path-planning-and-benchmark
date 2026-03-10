#!/usr/bin/env python3
"""
Benchmark Results Analyzer
- Merges multiple CSV files from parallel Docker containers.
- Computes success rates with Wilson confidence intervals.
- Runs Shapiro-Wilk normality tests.
- Runs Kruskal-Wallis + pairwise Mann-Whitney U tests.
- Generates publication-ready plots (boxplots, violin, success bar charts).
"""

import os
import sys
import glob
import argparse
import math

import pandas as pd
import numpy as np
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


def wilson_ci(n_success, n_total, z=1.96):
    """Compute Wilson score confidence interval for a proportion."""
    if n_total == 0:
        return 0.0, 0.0, 0.0
    p_hat = n_success / n_total
    denom = 1 + z**2 / n_total
    center = (p_hat + z**2 / (2 * n_total)) / denom
    spread = z * math.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n_total)) / n_total) / denom
    return p_hat, max(0, center - spread), min(1, center + spread)


def compute_success_rates(df, group_col="GlobalPlanner"):
    """Compute success rates per group with Wilson CI."""
    print(f"\n{'='*60}")
    print(f"  SUCCESS RATES (grouped by {group_col})")
    print(f"{'='*60}\n")

    results = []
    for name, group in df.groupby(group_col):
        n_total = len(group)
        n_success = len(group[group['Status'].str.upper() == 'SUCCESS']) if 'Status' in group.columns else 0
        rate, ci_low, ci_high = wilson_ci(n_success, n_total)
        results.append({
            group_col: name,
            'Total': n_total,
            'Success': n_success,
            'Rate': f"{rate:.1%}",
            '95% CI': f"[{ci_low:.1%}, {ci_high:.1%}]"
        })
        print(f"  {name:25s} | {n_success}/{n_total} = {rate:.1%}  CI: [{ci_low:.1%}, {ci_high:.1%}]")

    return pd.DataFrame(results)


def run_normality_tests(groups, metric_name):
    """Run Shapiro-Wilk test on each group."""
    print(f"\n=== Shapiro-Wilk Normality Test ({metric_name}) ===")
    print(f"H0: Data is normally distributed (p > 0.05)\n")
    for name, values in groups.items():
        if len(values) >= 3:
            stat, p = stats.shapiro(values)
            tag = "Normal" if p > 0.05 else "NOT Normal"
            print(f"  {name:25s} | W={stat:.4f}  p={p:.6f}  => {tag}")
        else:
            print(f"  {name:25s} | Too few samples ({len(values)})")


def run_kruskal_wallis(groups, metric_name):
    """Run Kruskal-Wallis H-test and pairwise Mann-Whitney U."""
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


def bootstrap_ci(data, n_bootstrap=10000, ci=0.95):
    """Compute bootstrap confidence interval for the mean."""
    if len(data) < 2:
        return np.mean(data), np.mean(data), np.mean(data)
    boot_means = np.array([
        np.mean(np.random.choice(data, size=len(data), replace=True))
        for _ in range(n_bootstrap)
    ])
    alpha = (1 - ci) / 2
    return np.mean(data), np.percentile(boot_means, alpha * 100), np.percentile(boot_means, (1 - alpha) * 100)


def analyze(df, group_col="GlobalPlanner", metrics=None):
    """Run full statistical analysis on the DataFrame."""
    if metrics is None:
        metrics = ["Time(s)", "Distance(m)", "Smoothness(rad)", "CPU(%)", "Memory(MiB)"]

    # Success rates first
    compute_success_rates(df, group_col)

    # Filter successful runs for metric analysis
    if "Status" in df.columns:
        successful = df[df["Status"].str.upper() == "SUCCESS"]
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

        # Descriptive stats with bootstrap CI
        print(f"\n--- Descriptive Statistics ---")
        desc = successful.groupby(group_col)[metric].describe()
        print(desc.to_string())

        print(f"\n--- 95% Bootstrap Confidence Intervals (Mean) ---")
        for name, group in successful.groupby(group_col):
            vals = group[metric].dropna().values
            if len(vals) >= 2:
                mean, ci_low, ci_high = bootstrap_ci(vals)
                print(f"  {name:25s} | Mean={mean:.4f}  95% CI: [{ci_low:.4f}, {ci_high:.4f}]")

        # Build groups for statistical tests
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


def generate_plots(df, group_col="GlobalPlanner", output_dir="results/figures"):
    """Generate publication-ready plots."""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
    except ImportError:
        print("Warning: matplotlib not available. Skipping plots.", file=sys.stderr)
        return

    os.makedirs(output_dir, exist_ok=True)

    if "Status" in df.columns:
        successful = df[df["Status"].str.upper() == "SUCCESS"]
    else:
        successful = df

    metrics = ["Time(s)", "Distance(m)", "Smoothness(rad)", "CPU(%)"]

    # Boxplots per metric
    for metric in metrics:
        if metric not in successful.columns:
            continue

        fig, ax = plt.subplots(figsize=(12, 6))
        groups = successful.groupby(group_col)[metric]
        data = [group.dropna().values for _, group in groups]
        labels = [name for name, _ in groups]

        bp = ax.boxplot(data, labels=labels, patch_artist=True)
        colors = plt.cm.Set2(np.linspace(0, 1, len(data)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_title(f'{metric} by {group_col}', fontsize=14, fontweight='bold')
        ax.set_ylabel(metric)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        fname = f"boxplot_{metric.replace('(', '').replace(')', '').replace('%', 'pct')}.png"
        plt.savefig(os.path.join(output_dir, fname), dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {fname}")

    # Violin plot for Time
    if "Time(s)" in successful.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        groups = successful.groupby(group_col)["Time(s)"]
        data = [group.dropna().values for _, group in groups]
        labels = [name for name, _ in groups]

        vp = ax.violinplot(data, showmeans=True, showmedians=True)
        ax.set_xticks(range(1, len(labels) + 1))
        ax.set_xticklabels(labels, rotation=45)
        ax.set_title('Time Distribution by Planner', fontsize=14, fontweight='bold')
        ax.set_ylabel('Time (s)')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "violin_time.png"), dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: violin_time.png")

    # Success rate bar chart
    if "Status" in df.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        rates = []
        ci_lows = []
        ci_highs = []
        labels = []
        for name, group in df.groupby(group_col):
            n_total = len(group)
            n_success = len(group[group['Status'].str.upper() == 'SUCCESS'])
            rate, ci_low, ci_high = wilson_ci(n_success, n_total)
            rates.append(rate * 100)
            ci_lows.append((rate - ci_low) * 100)
            ci_highs.append((ci_high - rate) * 100)
            labels.append(name)

        x = range(len(labels))
        colors = plt.cm.Set2(np.linspace(0, 1, len(labels)))
        bars = ax.bar(x, rates, yerr=[ci_lows, ci_highs], capsize=5,
                      color=colors, edgecolor='black', alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45)
        ax.set_ylabel('Success Rate (%)')
        ax.set_title('Success Rate by Planner (95% Wilson CI)', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 105)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "success_rate.png"), dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: success_rate.png")

    print(f"\nAll plots saved to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Analyze Benchmark Results")
    parser.add_argument("--results_dir", type=str, default=None,
                        help="Directory containing battery_summary_*.csv files")
    parser.add_argument("--summary_file", type=str, default=None,
                        help="Path to a single summary CSV (overrides --results_dir)")
    parser.add_argument("--group_by", type=str, default="GlobalPlanner",
                        help="Column to group by for comparison (default: GlobalPlanner)")
    parser.add_argument("--plot", action="store_true",
                        help="Generate publication-ready plots")
    parser.add_argument("--plot_dir", type=str, default="results/figures",
                        help="Output directory for plots (default: results/figures)")
    args = parser.parse_args()

    if args.summary_file:
        print(f"Analyzing single file: {args.summary_file}")
        df = pd.read_csv(args.summary_file)
    else:
        results_dir = args.results_dir or os.path.join(
            os.path.dirname(__file__), "..", "src", "plannie-main", "results"
        )
        df = find_and_merge_csvs(results_dir)

    # Save merged CSV
    if args.results_dir:
        merged_path = os.path.join(args.results_dir, "merged_results.csv")
        df.to_csv(merged_path, index=False)
        print(f"\nMerged CSV saved to: {merged_path}")

    analyze(df, group_col=args.group_by)

    if args.plot:
        print("\n--- Generating Plots ---")
        generate_plots(df, group_col=args.group_by, output_dir=args.plot_dir)


if __name__ == "__main__":
    main()
