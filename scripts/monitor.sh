#!/bin/bash
# Real-time Benchmark Progress Monitor

# Use the most recent results directory or a specific one provided as argument
RES_DIR=${1:-$(ls -dt results/run_* 2>/dev/null | head -n 1)}

if [ -z "$RES_DIR" ]; then
    echo "No results directory found in results/run_*"
    exit 1
fi

TOTAL_EXPECTED=1920

while true; do
  clear
  echo "============================================="
  echo "      Benchmarking Progress Monitor"
  echo "      Target: $RES_DIR"
  echo "============================================="

  CURRENT_COUNT=$(find "$RES_DIR" -name "*.csv" -exec grep -v "Scenario" {} + | wc -l 2>/dev/null || echo 0)
  PERCENT=$(( CURRENT_COUNT * 100 / TOTAL_EXPECTED ))
  BAR_SIZE=40
  COMPLETED=$(( CURRENT_COUNT * BAR_SIZE / TOTAL_EXPECTED ))
  REMAINING=$(( BAR_SIZE - COMPLETED ))
  
  printf "\e[1;34m📊 Current Stats\e[0m\n"
  printf "Concluído: $CURRENT_COUNT / $TOTAL_EXPECTED rodadas\n"
  printf "["
  for i in $(seq 1 $COMPLETED); do printf "\e[1;32m#\e[0m"; done
  for i in $(seq 1 $REMAINING); do printf "."; done
  printf "] $PERCENT%%\n"
  
  if [ $CURRENT_COUNT -ge $TOTAL_EXPECTED ]; then
    printf "\n\e[1;32m✅ BENCHMARK CONCLUÍDO!\e[0m\n"
    break
  fi
  sleep 10
done
