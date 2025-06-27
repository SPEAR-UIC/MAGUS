#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/UNet/"

cd ${benchmark_dir}
source UNet_env/bin/activate
# export OMP_NUM_THREADS=32
wandb offline
python train.py --amp -e 1

# torchrun --nproc_per_node=4 train.py --amp -e 1

deactivate
