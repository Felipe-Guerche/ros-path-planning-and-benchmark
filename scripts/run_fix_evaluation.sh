#!/bin/bash
GLOBAL_PLANNERS=("hybrid_astar" "lazy_theta_star")
LOCAL_PLANNERS=("apf" "dwa")
SCENARIOS=("static" "dynamic")
MASTER_SEED="15257"
NUM_RUNS=40

for scenario in "${SCENARIOS[@]}"; do
    for global in "${GLOBAL_PLANNERS[@]}"; do
        for local in "${LOCAL_PLANNERS[@]}"; do
            echo ">>> Rodando Re-avaliação Corrigida: $global + $local ($scenario)"
            docker run --rm \
                -e SINGLE_GLOBAL_PLANNER="$global" \
                -e SINGLE_LOCAL_PLANNER="$local" \
                -e SINGLE_SCENARIO="$scenario" \
                -e SINGLE_NUM_RUNS="$NUM_RUNS" \
                -e MASTER_SEED="$MASTER_SEED" \
                -v "$(pwd):/project" \
                ros-benchmark-noetic
        done
    done
done
