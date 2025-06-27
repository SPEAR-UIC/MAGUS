#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS
# suite 2: npb


suite=0
g_cap=1
power_shift=0


# Set suite_dir based on suite value
if [ $suite -eq 0 ]; then
    suite_dir="ecp_power_res"
elif [ $suite -eq 1 ]; then
    suite_dir="altis_power_res"
elif [ $suite -eq 2 ]; then
    suite_dir="npb_power_res"
else
    echo "Invalid suite value"
    exit 1
fi

if [ $power_shift -eq 0 ]; then
    shift_dir="noShift"
else
    shift_dir="shift"
fi



# ################################ dynamic_uncore, cap ################################ 
# sudo nvidia-smi -pl 150

# python3 exp_power_motif.py --suite $suite --test 0 --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 1 --uncore_0 0.8 --uncore_1 0.8 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --power_shift $power_shift  --g_cap $g_cap 

# sudo nvidia-smi -pl 250

# sleep 10
# sudo mv /home/cc/power/GPGPU/data/$suite_dir/cap/$shift_dir/*.csv /home/cc/power/GPGPU/data/$suite_dir/cap/$shift_dir/dynamic_uncore

# sudo mv /home/cc/power/GPGPU/data/$suite_dir/cap/$shift_dir/mem_throughput/*.csv /home/cc/power/GPGPU/data/$suite_dir/cap/$shift_dir/mem_throughput/dynamic_uncore



######################### max_uncore, cap ################################ 
sudo nvidia-smi -pl 150

python3 exp_power_motif.py --suite $suite --test 0 --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.4 --uncore_1 2.4 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --power_shift $power_shift  --g_cap $g_cap 

sudo nvidia-smi -pl 250

sleep 10
sudo mv /home/cc/power/GPGPU/data/$suite_dir/cap/$shift_dir/*.csv /home/cc/power/GPGPU/data/$suite_dir/cap/$shift_dir/max_uncore

sudo mv /home/cc/power/GPGPU/data/$suite_dir/cap/$shift_dir/mem_throughput/*.csv /home/cc/power/GPGPU/data/$suite_dir/cap/$shift_dir/mem_throughput/max_uncore



TARGET_DIR="../data/"

# Find all .csv files under the target directory and make them writable
sudo find "$TARGET_DIR" -type f -name "*.csv" -exec chown $(whoami):$(whoami) {} \;





