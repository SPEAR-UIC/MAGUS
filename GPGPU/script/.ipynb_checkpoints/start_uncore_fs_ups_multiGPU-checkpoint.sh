#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS
# suite 2: npb

# CARDL: 200, 500, 3
# UNet:  200, 500, 5
# miniGAN 200, 500, 5
# sw4lite 200, 500, 5
# Laghos 200, 500, 5
# XSBench 200, 500, 5
#lammps 200,500,5

################### ECP Starts ###################


python3 exp_power_motif.py --suite 0 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.2 --uncore_1 2.2 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 1 --burst_up 0.4 --burst_low 0.2 --ups 1 --benchmark gromacs

# sleep 5

# sudo mv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/*.csv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/multiGPU/ups_uncore 
# sudo mv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/mem_throughput/*.csv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/multiGPU/mem_throughput/ups_uncore


################### ECP Ends ###################




./power_util/set_uncore_freq.sh 2.4 2.4





TARGET_DIR="../data/"

# Find all .csv files under the target directory and make them writable
sudo find "$TARGET_DIR" -type f -name "*.csv" -exec chown $(whoami):$(whoami) {} \;