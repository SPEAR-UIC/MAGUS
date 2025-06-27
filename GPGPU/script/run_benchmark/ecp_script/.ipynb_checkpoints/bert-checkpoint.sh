#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/bert/"

cd ${benchmark_dir}
source /home/cc/benchmark/ECP/UNet/UNet_env/bin/activate
python train.py 

deactivate
