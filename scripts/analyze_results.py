#!/usr/bin/env python3
"""
Benchmark Results Analyzer
- Merges multiple CSV files from parallel Docker containers.
- Computes success rates with Wilson confidence intervals.
- Runs Shapiro-Wilk normality tests.
- Runs Kruskal-Wallis + pairwise Mann-Whitney U tests.
- Generates publication-ready plots with Strict Variable Isolation.
"""

import os
import sys
import glob
import argparse
import math

import pandas as pd
import numpy as np
from scipy import stats

try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
except ImportError:
    sns = None
    plt = None

# Publication-Standard Palette Mapping
PALETTE_MAP = {
    "astar": "#1f77b4",          # Blue
    "hybrid_astar": "#ff7f0e",   # Orange
    "dijkstra": "#2ca02c",       # Green
    "lazy_theta_star": "#d62728",# Red
    "dstar_lite": "#9467bd",     # Purple
    "rrt": "#8c564b",            # Brown
    "unknown": "#7f7f7f"         # Gray
}

# Nominal Scenario for Tier 1 "Article" Plots
NOMINAL_CONFIG = {
    "InflationFactor": 0.5,
    "PedCount": 5
}


def find_and_merge_csvs(results_dir):
    """Find all summary CSV files, merge, and create rigorous statistical groups."""
    # Updated pattern to catch both legacy and new Pause & Resume deterministic names
    pattern = os.path.join(results_dir, "*summary_*.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No summary files found in: {results_dir}")
        sys.exit(1)

    print(f"Found {len(files)} summary file(s):")
    for f in files:
        print(f"  - {os.path.basename(f)}")

    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f)
            if df.empty:
                print(f"  [WARN] Skipping empty file: {os.path.basename(f)}")
                continue
            dfs.append(df)
        except Exception as e:
            print(f"  [WARN] Could not read {os.path.basename(f)}: {e}. Skipping.")

    if not dfs:
        print("No readable summary files found. Aborting.")
        sys.exit(1)

    df = pd.concat(dfs, ignore_index=True)
    df["Algorithm"] = df["GlobalPlanner"] + "-" + df["LocalPlanner"]

    # ---------------------------------------------------------
    # Strict Variable Isolation
    # Avoid mixing different scenarios/sweeps in the same distribution
    # ---------------------------------------------------------
    cols_to_group = []
    potential_vars = ["Scenario", "GlobalPlanner", "LocalPlanner", "PedCount", "InflationFactor", "SweepParam"]

    for col in potential_vars:
        if col in df.columns:
            cols_to_group.append(col)

    if cols_to_group:
        df["Config_Tag"] = df[cols_to_group].astype(str).agg('-'.join, axis=1)
    elif "GlobalPlanner" in df.columns:
        df["Config_Tag"] = df["GlobalPlanner"]
    else:
        df["Config_Tag"] = "UnknownGroup"

    # ---------------------------------------------------------
    # Strict Variable Isolation
    # ---------------------------------------------------------
    # Extract extra parameters from Config_Tag if not present
    for col in ["InflationFactor", "PedCount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            # Try to extract from Config_Tag: e.g. "dynamic-astar-dwa-PEDS-INFLATION-..."
            def extract_param(tag, param_type):
                parts = str(tag).split('-')
                if len(parts) >= 6:
                    if param_type == "PedCount": return float(parts[3])
                    if param_type == "InflationFactor": return float(parts[4])
                return np.nan
            df[col] = df["Config_Tag"].apply(lambda x: extract_param(x, col))
    
    print(f"\nTotal rows after merge: {len(df)}")
    print(f"Identified {df['Config_Tag'].nunique()} unique experimental conditions.")
    return df


def wilson_ci(n_success, n_total, z=1.96):
    """Compute Wilson score confidence interval for a proportion."""
    if n_total == 0:
        return 0.0, 0.0, 0.0
    p_hat = n_success / n_total
    denom = 1 + z**2 / n_total
    center = (p_hat + z**2 / (2 * n_total)) / denom
    spread = z * math.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n_total)) / n_total) / denom
    return p_hat, max(0, center - spread), min(1, center + spread)


def compute_success_rates(df, group_col="Config_Tag"):
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
        print(f"  {name:40s} | {n_success:3d}/{n_total:<3d} = {rate:>6.1%}  CI: [{ci_low:.1%}, {ci_high:.1%}]")

    return pd.DataFrame(results)


def run_normality_tests(groups, metric_name):
    """Run Shapiro-Wilk test on each group."""
    print(f"\n=== Shapiro-Wilk Normality Test ({metric_name}) ===")
    print(f"H0: Data is normally distributed (p > 0.05)\n")
    for name, values in groups.items():
        if len(values) >= 3:
            stat, p = stats.shapiro(values)
            tag = "Normal" if p > 0.05 else "NOT Normal"
            print(f"  {name:40s} | W={stat:.4f}  p={p:.6f}  => {tag}")
        else:
            print(f"  {name:40s} | Too few samples ({len(values)})")


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
                print(f"  {names[i][:20]:20s} vs {names[j][:20]:20s} | U={u_stat:>6.1f}  p={u_p:.6f}  => {tag}")
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


def analyze(df, group_col="Config_Tag", metrics=None):
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
                print(f"  {name:40s} | Mean={mean:.4f}  95% CI: [{ci_low:.4f}, {ci_high:.4f}]")

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


def report_failures(df, output_dir):
    """Identify and log specific failure cases by Seed for each configuration."""
    if "Status" not in df.columns or "Seed" not in df.columns:
        return

    failures = df[df["Status"].str.upper() != "SUCCESS"]
    if failures.empty:
        print("\nNo failure cases detected. All runs successful!")
        return

    report_path = os.path.join(output_dir, "failure_report.txt")
    print(f"\nFound {len(failures)} failure cases. Generating report: {report_path}")

    with open(report_path, "w") as f:
        f.write("==========================================================\n")
        f.write("       BENCHMARK FAILURE CASE REPORT (SEED ANALYSIS)\n")
        f.write("==========================================================\n\n")
        f.write(f"Total Failures: {len(failures)} / {len(df)}\n\n")

        for name, group in failures.groupby("Config_Tag"):
            f.write(f"--- Configuration: {name} ---\n")
            f.write(f"  Failures: {len(group)}\n")
            seeds = sorted(group["Seed"].unique().tolist())
            f.write(f"  Problematic Seeds: {', '.join(map(str, seeds))}\n")
            f.write("\n")

    print(f"Failure report generated successfully.")


def get_algo_color(planner_name):
    """Map planner names to consistent palette colors."""
    p_lower = str(planner_name).lower()
    for key, color in PALETTE_MAP.items():
        if key in p_lower:
            return color
    return PALETTE_MAP["unknown"]


def generate_plots(df, group_col="Config_Tag", output_dir="results/figures"):
    """Generate publication-ready, two-tier plots using Seaborn."""
    if not sns or not plt:
        print("Warning: seaborn/matplotlib not available. Skipping plots.", file=sys.stderr)
        return

    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="white")
    
    # Pre-process Data: Add combined Algo tag and handle Smoothness outliers
    df["Algorithm"] = df["GlobalPlanner"] + "-" + df["LocalPlanner"]
    
    # Tier 1 & 2 Metrics
    metrics = ["Time(s)", "Distance(m)", "Smoothness(rad)", "CPU(%)", "Memory(MiB)"]
    
    # Build dynamic palette from Algorithm column
    active_algos = df["Algorithm"].unique()
    algo_palette = {algo: get_algo_color(algo) for algo in active_algos}
    
    # ---------------------------------------------------------
    # TIER 1: Article-Ready Overview (Nominal Case)
    # ---------------------------------------------------------
    print("\n[Vizu] Generating Tier 1: Article-Ready Overview (Nominal Case)...")
    tier1_dir = os.path.join(output_dir, "tier1_article")
    os.makedirs(tier1_dir, exist_ok=True)

    # Filtering for nominal case (e.g., Inflation=0.5, PedCount=5 or closest)
    # Handle both Static (PedCount=0 typically) and Dynamic
    nominal_df = df[
        ((df["Scenario"] == "static") & (df["InflationFactor"] == 0.5)) |
        ((df["Scenario"] == "dynamic") & (df["InflationFactor"] == 0.5) & (df["PedCount"] == 5))
    ]
    
    if nominal_df.empty:
        print("  [WARN] No exact nominal matches found. Relaxing filter to Inflation=0.5.")
        nominal_df = df[df["InflationFactor"] == 0.5] if "InflationFactor" in df.columns else df

    succ_nom = nominal_df[nominal_df["Status"].str.upper() == "SUCCESS"]
    
    for metric in metrics:
        if metric not in succ_nom.columns:
            continue
            
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Determine scale limits for Smoothness to avoid compression by RRT outliers
        y_limit = None
        if metric == "Smoothness(rad)":
            q3 = succ_nom[metric].quantile(0.75)
            iqr = q3 - succ_nom[metric].quantile(0.25)
            y_limit = q3 + 5.0 * iqr # Cap at 5*IQR for visibility
            
        # Draw Boxplot
        sns.boxplot(data=succ_nom, x="Algorithm", y=metric, hue="Algorithm", 
                    palette=algo_palette, ax=ax, showmeans=True,
                    meanprops={"marker":"*", "markerfacecolor":"white", "markeredgecolor":"black"},
                    dodge=False)
        
        if y_limit:
            ax.set_ylim(0, y_limit)
            ax.set_title(f"{metric} (Outliers Capped for Visibility)", fontweight='bold')
        else:
            ax.set_title(f"{metric} - Nominal Case Analysis", fontweight='bold')
            
        ax.set_xlabel("Planner Combination")
        ax.set_ylabel(metric)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save as PDF (Vector) and PNG (Review)
        metric_safe = metric.replace('(', '').replace(')', '').replace('%', 'pct')
        fig.savefig(os.path.join(tier1_dir, f"{metric_safe}.pdf"), format='pdf')
        fig.savefig(os.path.join(tier1_dir, f"{metric_safe}.png"), dpi=300)
        plt.close()

    # ---------------------------------------------------------
    # TIER 2: Parameter Sensitivity (Appendix Facets)
    # ---------------------------------------------------------
    print("[Vizu] Generating Tier 2: Parameter Sensitivity (Appendix Facets)...")
    tier2_dir = os.path.join(output_dir, "tier2_sensitivity")
    os.makedirs(tier2_dir, exist_ok=True)
    
    succ_df = df[df["Status"].str.upper() == "SUCCESS"]
    
    for metric in metrics:
        if metric not in succ_df.columns:
            continue
            
        metric_safe = metric.replace('(', '').replace(')', '').replace('%', 'pct')

        # 2a. Static Sensitivity (Only Inflation varies)
        static_succ = succ_df[succ_df["Scenario"] == "static"]
        if not static_succ.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=static_succ, x="Algorithm", y=metric, hue="InflationFactor",
                        palette="viridis", ax=ax)
            ax.set_title(f"Sensitivity: Static Environment - {metric}", fontweight='bold')
            plt.xticks(rotation=45)
            plt.tight_layout()
            fig.savefig(os.path.join(tier2_dir, f"static_sens_{metric_safe}.pdf"), format='pdf')
            fig.savefig(os.path.join(tier2_dir, f"static_sens_{metric_safe}.png"), dpi=300)
            plt.close()

        # 2b. Dynamic Sensitivity (Faceted by PedCount)
        dynamic_succ = succ_df[succ_df["Scenario"] == "dynamic"]
        if not dynamic_succ.empty:
            # We filter out Peds 0 from dynamic if it's redundant with static
            # but usually dynamic starts at 3 peds in this benchmark
            g = sns.catplot(
                data=dynamic_succ, x="Algorithm", y=metric,
                hue="InflationFactor", col="PedCount", col_wrap=2,
                kind="box", palette="viridis", 
                height=5, aspect=1.2, sharey=False,
                margin_titles=True
            )
            g.set_axis_labels("Planner", metric)
            g.set_titles("Dynamic Env - {col_name} Pedestrians", fontweight='bold')
            for ax in g.axes.flat:
                for label in ax.get_xticklabels():
                    label.set_rotation(45)
            
            g.savefig(os.path.join(tier2_dir, f"dynamic_sens_{metric_safe}.pdf"), format='pdf')
            g.savefig(os.path.join(tier2_dir, f"dynamic_sens_{metric_safe}.png"), dpi=300)
            plt.close()

    # ---------------------------------------------------------
    # SUCCESS RATES (Article Ready Comparison)
    # ---------------------------------------------------------
    print("[Vizu] Generating Success Rate Comparisons...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Compute rates on nominal set
    res_list = []
    for name, group in nominal_df.groupby("Algorithm"):
        rate, ci_low, ci_high = wilson_ci(len(group[group['Status'].str.upper() == 'SUCCESS']), len(group))
        res_list.append({"Algorithm": name, "Success Rate (%)": rate * 100, "CI_Low": ci_low*100, "CI_High": ci_high*100})
    
    rate_df = pd.DataFrame(res_list)
    
    # Custom error bars with Seaborn/Matplotlib
    sns.barplot(data=rate_df, x="Algorithm", y="Success Rate (%)", palette=algo_palette, ax=ax, edgecolor=".2")
    
    # Add error segments manually for Wilson CI
    for i, row in rate_df.iterrows():
        ax.errorbar(i, row["Success Rate (%)"], yerr=[[row["Success Rate (%)"] - row["CI_Low"]], [row["CI_High"] - row["Success Rate (%)"]]],
                    fmt='none', c='black', capsize=5)

    ax.set_title("Overall Success Rate (Nominal Scenario, 95% Wilson CI)", fontweight='bold')
    ax.set_ylim(0, 105)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(tier1_dir, "success_rate.pdf"), format='pdf')
    plt.savefig(os.path.join(tier1_dir, "success_rate.png"), dpi=300)
    plt.close()

    print(f"\n[Vizu] All plots saved to: {output_dir}")
    print(f"  - Tier 1 (Paper): {tier1_dir}")
    print(f"  - Tier 2 (Appendix): {tier2_dir}")

    print(f"\nAll plots saved to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Analyze Benchmark Results")
    parser.add_argument("--results_dir", type=str, default=None,
                        help="Directory containing summary_*.csv files")
    parser.add_argument("--summary_file", type=str, default=None,
                        help="Path to a single summary CSV (overrides --results_dir)")
    parser.add_argument("--group_by", type=str, default="Config_Tag",
                        help="Column to group by (default: Config_Tag, dynamically generated)")
    parser.add_argument("--plot", action="store_true",
                        help="Generate publication-ready plots")
    parser.add_argument("--plot_dir", type=str, default=None,
                        help="Output directory for plots (default: <results_dir>/figures)")
    args = parser.parse_args()

    # Load Data
    if args.summary_file:
        print(f"Analyzing single file: {args.summary_file}")
        df = pd.read_csv(args.summary_file)
        if "Config_Tag" not in df.columns and args.group_by == "Config_Tag":
            df["Config_Tag"] = df["GlobalPlanner"] if "GlobalPlanner" in df.columns else "Unknown"
    else:
        results_dir = args.results_dir or os.path.join(
            os.path.dirname(__file__), "..", "src", "plannie-main", "results"
        )
        df = find_and_merge_csvs(results_dir)

    # Save merged output
    if args.results_dir:
        merged_path = os.path.join(args.results_dir, "merged_results.csv")
        df.to_csv(merged_path, index=False)

    # Run Analysis
    analyze(df, group_col=args.group_by)

    # Report Failures
    report_failures(df, args.results_dir or os.path.dirname(merged_path))

    # Run Plots
    if args.plot:
        print("\n--- Generating Plots ---")
        plot_dir = args.plot_dir or os.path.join(results_dir, "figures")
        generate_plots(df, group_col=args.group_by, output_dir=plot_dir)


if __name__ == "__main__":
    main()
