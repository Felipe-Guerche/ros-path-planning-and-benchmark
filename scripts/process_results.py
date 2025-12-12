#!/usr/bin/env python3

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def process_results(results_dir, output_file):
    """
    Scans the results directory for summary CSVs and individual run files.
    Aggregates data and generates basic plots.
    """
    print(f"Scanning results in: {results_dir}")
    
    # Example logic: Read the latest summary file
    summary_files = glob.glob(os.path.join(results_dir, "battery_summary_*.csv"))
    if not summary_files:
        print("No summary files found.")
        return

    # Sort by time, pick latest
    latest_summary = max(summary_files, key=os.path.getctime)
    print(f"Processing latest summary: {latest_summary}")
    
    try:
        df = pd.read_csv(latest_summary)
        print("Summary Data Preview:")
        print(df.head())
        
        # Basic Analysis example
        if 'Time(s)' in df.columns and 'GlobalPlanner' in df.columns:
            print("\nAverage Time per Global Planner:")
            print(df.groupby('GlobalPlanner')['Time(s)'].mean())

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Plannie Benchmark Results")
    parser.add_argument("--results_dir", type=str, default="../src/plannie-main/results", help="Path to results directory")
    parser.add_argument("--output", type=str, default="analysis_report.pdf", help="Output filename for plots")
    
    args = parser.parse_args()
    process_results(args.results_dir, args.output)
