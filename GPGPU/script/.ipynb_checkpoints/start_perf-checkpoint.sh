#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS
# suite 2: npb

# 0 for big
# 1 for small

# # test
# ./power_util/cpu_cap.sh 250
# ./power_util/gpu_cap.sh 260

# sudo python3 exp_performance.py --suite 2 --test 0 --benchmark_size 0
python3 exp_perf.py --suite 1 --test 0 --benchmark_size 0


