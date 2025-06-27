# Minimizing Power Waste in Heterogenous Computing via Adaptive Uncore Scaling

## Setup environment
./setup.sh

## Start MAGUS as a background process with sudo 
sudo ./src/build/bin/pcm-memory 0.1 --uncore_0 0.8 --uncore_1 0.8 --dynamic_ufs_mem 1 --inc_ts 300
--dec_ts 500 --history 5 --burst_up 0.4 &


## Run application for example
./raytracing --passes 1 -s 4


## Result Reproducing
./start_uncore_fs.sh   
reuslts are saved in ./GPGPU/data  
use uncore_fs.ipynb to plot

## Note
Please change hard-coded dir path to your own path. 
i.e., in pcm-memory.c, start_uncore_fs.sh, exp_power_motif.py
