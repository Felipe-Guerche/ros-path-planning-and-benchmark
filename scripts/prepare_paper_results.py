#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import os

def wilson_ci(n_success, n_total, z=1.96):
    if n_total == 0:
        return 0.0, 0.0
    p_hat = n_success / n_total
    denom = 1 + z**2 / n_total
    center = (p_hat + z**2 / (2 * n_total)) / denom
    spread = z * math.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n_total)) / n_total) / denom
    return max(0, center - spread), min(1, center + spread)

def format_planner_name(global_p, local_p):
    name_map = {
        'astar': 'A*',
        'hybrid_astar': 'Hybrid A*',
        'dijkstra': 'Dijkstra',
        'lazy_theta_star': 'Lazy Theta*',
        'dstar_lite': 'D* Lite',
        'rrt': 'RRT'
    }
    g = name_map.get(global_p, global_p.replace('_', ' ').title())
    l = local_p.upper()
    return f"{g} + {l}"

import glob

def find_and_merge_results(results_dir):
    # 1. Collect all root summaries
    pattern_root = os.path.join(results_dir, "battery_summary_*.csv")
    files_root = glob.glob(pattern_root)
    
    # 2. Collect all backup summaries
    pattern_backup = os.path.join(results_dir, "backup_anomalies", "battery_summary_*.csv")
    files_backup = glob.glob(pattern_backup)
    
    # We want to use backup files if they exist, otherwise use root files.
    # Map from filename to full path, prioritizing backup.
    final_files_map = {}
    
    for f in files_root:
        final_files_map[os.path.basename(f)] = f
        
    for f in files_backup:
        # This will overwrite the root path with the backup path for the same filename
        final_files_map[os.path.basename(f)] = f
    
    print(f"Merging {len(final_files_map)} files (prioritizing {len(files_backup)} from backup_anomalies)...")
    
    dfs = []
    for fname, fpath in final_files_map.items():
        try:
            df_tmp = pd.read_csv(fpath, on_bad_lines='skip')
            if not df_tmp.empty:
                dfs.append(df_tmp)
        except Exception as e:
            print(f"Warning: Could not read {fpath}: {e}")
    
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)

# Load data
results_dir = 'results/seed_15257/'
df = find_and_merge_results(results_dir)

if df.empty:
    print("Error: No data loaded.")
    sys.exit(1)

# Overwrite final summary for consistency (Authoritative Source)
df.to_csv('results/seed_15257/merges/final_summary_seed_15257.csv', index=False)
print("Updated results/seed_15257/merges/final_summary_seed_15257.csv with complete dataset.")

# Ensure numeric types
metrics = ['Status', 'Time(s)', 'Distance(m)', 'Smoothness(rad)', 'CPU(%)', 'Memory(MiB)', 'Memory(%)']
for m in metrics[1:]:
    df[m] = pd.to_numeric(df[m], errors='coerce')

# Global sorting order for planners
PLANNER_ORDER = [
    'Dijkstra + APF', 'Dijkstra + DWA', 
    'A* + APF', 'A* + DWA',
    'D* Lite + APF', 'D* Lite + DWA',
    'RRT + APF', 'RRT + DWA',
    'Hybrid A* + APF', 'Hybrid A* + DWA',
    'Lazy Theta* + APF', 'Lazy Theta* + DWA'
]

# Filter for nominal dynamic case (Table II: 3 peds, 0.5 inflation)
# The user request mentions seed_15257 specifically.
df_dynamic = df[(df['Scenario'] == 'dynamic') & (df['PedCount'] == 3) & (df['InflationFactor'] == 0.5)]

# Table II Generation
table_results = []
for (gp, lp), group in df_dynamic.groupby(['GlobalPlanner', 'LocalPlanner']):
    n_total = len(group)
    n_success = len(group[group['Status'].str.upper() == 'SUCCESS'])
    rate = n_success / n_total if n_total > 0 else 0
    ci_low, ci_high = wilson_ci(n_success, n_total)
    
    succ_group = group[group['Status'].str.upper() == 'SUCCESS']
    if not succ_group.empty:
        mean_time = succ_group['Time(s)'].mean()
        mean_cpu = succ_group['CPU(%)'].mean()
        mean_mem = succ_group['Memory(MiB)'].mean()
        mean_smooth = succ_group['Smoothness(rad)'].mean()
    else:
        # For planners with 0 success, use mean of all as fallback (typically timeout)
        mean_time = group['Time(s)'].mean()
        mean_cpu = group['CPU(%)'].mean()
        mean_mem = group['Memory(MiB)'].mean()
        mean_smooth = group['Smoothness(rad)'].mean()

    table_results.append({
        'Configuration': format_planner_name(gp, lp),
        'Success': rate * 100,
        'CI_Err': (ci_high - rate) * 100,
        'Time': mean_time,
        'CPU': mean_cpu,
        'RAM': mean_mem,
        'Smoothness': mean_smooth
    })

res_df = pd.DataFrame(table_results)
res_df['SortKey'] = res_df['Configuration'].apply(lambda x: PLANNER_ORDER.index(x) if x in PLANNER_ORDER else 99)
res_df = res_df.sort_values('SortKey').drop(columns=['SortKey'])

print("--- LaTeX Table Snippet ---")
for _, row in res_df.iterrows():
    print(f"{row['Configuration']} & ${row['Success']:.1f} \\pm {row['CI_Err']:.1f}$ & ${row['Time']:.1f}$ & ${row['CPU']:.1f}$ & ${row['RAM']:.1f}$ & ${row['Smoothness']:.1f}$ \\\\")

# Figure: Primary Metrics (success_rate.png, Times.png, Distancem.png)
# These should be based on the same nomadic dynamic case (PedCount=3, Inflation=0.5)

# 1. Success Rate
plt.figure(figsize=(10, 6))
# Pre-sort for consistency
succ_df = res_df.copy()
sns.barplot(data=succ_df, x='Configuration', y='Success', palette='viridis')
# Add error bars
for i, row in succ_df.iterrows():
    plt.errorbar(i, row['Success'], yerr=row['CI_Err'], fmt='none', c='black', capsize=5)
plt.title('Success Rate (95% Wilson CI)', fontweight='bold')
plt.ylabel('Success (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('article/figures/success_rate.png', dpi=300)
plt.close()

# 2. Execution Time (Boxplot)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_dynamic[df_dynamic['Status'].str.upper() == 'SUCCESS'], 
            x=df_dynamic[df_dynamic['Status'].str.upper() == 'SUCCESS'].apply(lambda r: format_planner_name(r['GlobalPlanner'], r['LocalPlanner']), axis=1), 
            y='Time(s)', palette='viridis', order=PLANNER_ORDER)
plt.title('Execution Time Distribution (s)', fontweight='bold')
plt.xlabel('Configuration')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('article/figures/Times.png', dpi=300)
plt.close()

# 3. Distance (Boxplot)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_dynamic[df_dynamic['Status'].str.upper() == 'SUCCESS'], 
            x=df_dynamic[df_dynamic['Status'].str.upper() == 'SUCCESS'].apply(lambda r: format_planner_name(r['GlobalPlanner'], r['LocalPlanner']), axis=1), 
            y='Distance(m)', palette='viridis', order=PLANNER_ORDER)
plt.title('Path Length/Distance (m)', fontweight='bold')
plt.xlabel('Configuration')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('article/figures/Distancem.png', dpi=300)
plt.close()

# Figure: Heatmap (Aggregated Results for Seed 15257)
# Use allPedCounts or just nomadic? 
# The figure in LaTeX (fig:heatmap) title says "Aggregated Results (Seed 15257)".
# Typically this averages over all ped counts and inflation?
# Let's check the figure caption: "Planner Performance Matrix for the dynamic scenario".
df_all_dynamic = df[df['Scenario'] == 'dynamic'].copy()
df_all_dynamic['Configuration'] = df_all_dynamic.apply(lambda r: format_planner_name(r['GlobalPlanner'], r['LocalPlanner']), axis=1)

heatmap_data = []
for config, group in df_all_dynamic.groupby('Configuration'):
    n_total = len(group)
    n_success = len(group[group['Status'].str.upper() == 'SUCCESS'])
    rate = n_success / n_total
    
    # Successful metrics
    succ = group[group['Status'].str.upper() == 'SUCCESS']
    if not succ.empty:
        heatmap_data.append({
            'Planner': config,
            'Success (%)': rate * 100,
            'Time(s)': succ['Time(s)'].mean(),
            'Distance(m)': succ['Distance(m)'].mean(),
            'CPU(%)': succ['CPU(%)'].mean(),
            'Memory(MiB)': succ['Memory(MiB)'].mean()
        })
    else:
        heatmap_data.append({
            'Planner': config,
            'Success (%)': 0.0,
            'Time(s)': group['Time(s)'].mean(),
            'Distance(m)': group['Distance(m)'].mean(),
            'CPU(%)': group['CPU(%)'].mean(),
            'Memory(MiB)': group['Memory(MiB)'].mean()
        })

h_df = pd.DataFrame(heatmap_data).set_index('Planner')
h_df = h_df.reindex(PLANNER_ORDER[::-1]) # Reversed for heatmap top-down

# Normalize for colors (Relative Performance)
# Success: higher is better
# Others: lower is better
h_norm = h_df.copy()
h_norm['Success (%)'] = (h_df['Success (%)'] - h_df['Success (%)'].min()) / (h_df['Success (%)'].max() - h_df['Success (%)'].min() + 1e-9)
for col in ['Time(s)', 'Distance(m)', 'CPU(%)', 'Memory(MiB)']:
    h_norm[col] = (h_df[col].max() - h_df[col]) / (h_df[col].max() - h_df[col].min() + 1e-9)

plt.figure(figsize=(12, 10))
sns.heatmap(h_norm, annot=h_df, fmt='.1f', cmap='RdYlGn', cbar_kws={'label': 'Relative Performance (Green = Best)'})
plt.title('Planner Performance Matrix (Dynamic Scenario)\nAggregated Results (Seed 15257)', fontweight='bold')
plt.tight_layout()
plt.savefig('article/figures/plot_heatmap.png', dpi=300)
plt.close()

# Figure: Efficiency (Time vs CPU Aggregated)
h_df_sorted = h_df.sort_values('Time(s)') # Faster planners first
fig, ax1 = plt.subplots(figsize=(12, 6))

color_time = '#8da0cb'
color_cpu = '#d6604d'

ax1.bar(h_df_sorted.index, h_df_sorted['Time(s)'], color=color_time, alpha=0.7, label='Mean Execution Time')
ax1.set_xlabel('Planner Configuration')
ax1.set_ylabel('Mean Execution Time (s)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
plt.xticks(rotation=45, ha='right')

ax2 = ax1.twinx()
ax2.plot(h_df_sorted.index, h_df_sorted['CPU(%)'], color=color_cpu, marker='D', linewidth=2, label='Mean CPU Usage')
ax2.set_ylabel('Mean CPU Usage (%)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title('Computational Efficiency: Time vs CPU Load (Aggregated)', fontweight='bold')
plt.tight_layout()
plt.savefig('article/figures/plot_efficiency_cpu.png', dpi=300)
plt.close()

print("\nFigures generated in article/figures/")
