#!/bin/bash

# Define parameter ranges
inc_ts_vals=(100 300 500 700 900 1100 1300 1500 1700 1900)
dec_ts_vals=(100 300 500 700 900 1100 1300 1500 1700 1900)
burst_up_vals=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0)
memory_throughput_ts_vals=(20000 40000 60000 80000 100000 120000 140000 160000 180000 200000)

# Default values
default_inc_ts=300
default_dec_ts=500
default_burst_up=0.4
default_memory_throughput_ts=40000

# Benchmark list
benchmarks=(
    "bfs" "gemm" "pathfinder" "sort" "cfd" "cfd_double" "fdtd2d"
    "kmeans" "lavamd" "nw" "particlefilter_float" "raytracing" "where"
)

target_dir="/home/cc/power/GPGPU/data/sensitivity"

run_experiment () {
    local inc_ts=$1
    local dec_ts=$2
    local burst_up=$3
    local memory_throughput_ts=$4
    local benchmark=$5

    echo "Running: $benchmark | inc_ts=$inc_ts, dec_ts=$dec_ts, burst_up=$burst_up, memory_throughput_ts=$memory_throughput_ts"

    python3 exp_power_motif.py --suite 1 --test 0 --dynamic_ufs_gpuP 0 \
        --dynamic_ufs_mem 1 --uncore_0 0.8 --uncore_1 0.8 --pcm 1 \
        --inc_ts "$inc_ts" --dec_ts "$dec_ts" --history 5 --dual_cap 1 \
        --burst_up "$burst_up" --burst_low 0.2 \
        --memory_throughput_ts "$memory_throughput_ts" --ups 0 \
        --benchmark "$benchmark"

    sleep 2

    # Build key for suffix
    key="${inc_ts}_${dec_ts}_${burst_up}_${memory_throughput_ts}"

    for file in /home/cc/power/GPGPU/data/altis_power_res/no_power_shift/*.csv; do
        if [[ -f "$file" ]]; then
            filename=$(basename "$file" .csv)
            new_file="${target_dir}/${benchmark}/${filename}_${key}.csv"
            sudo mv "$file" "$new_file"
        fi
    done
}

# === Run experiments for all benchmarks ===
for benchmark in "${benchmarks[@]}"; do
    echo "=== Running experiments for: $benchmark ==="

    # Create folder for this benchmark if not exists
    mkdir -p "${target_dir}/${benchmark}"

    # Vary inc_ts
    for val in "${inc_ts_vals[@]}"; do
        run_experiment "$val" "$default_dec_ts" "$default_burst_up" "$default_memory_throughput_ts" "$benchmark"
    done

    # Vary dec_ts
    for val in "${dec_ts_vals[@]}"; do
        run_experiment "$default_inc_ts" "$val" "$default_burst_up" "$default_memory_throughput_ts" "$benchmark"
    done

    # Vary burst_up
    for val in "${burst_up_vals[@]}"; do
        run_experiment "$default_inc_ts" "$default_dec_ts" "$val" "$default_memory_throughput_ts" "$benchmark"
    done

    # Vary memory_throughput_ts
    for val in "${memory_throughput_ts_vals[@]}"; do
        run_experiment "$default_inc_ts" "$default_dec_ts" "$default_burst_up" "$val" "$benchmark"
    done

    # Fix ownership
    sudo chown -R $(whoami):$(whoami) "${target_dir}/${benchmark}"
done
