#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/Resnet50/"

source ${home_dir}/benchmark/ECP/UNet/UNet_env/bin/activate

cd ${benchmark_dir}
python train.py 

deactivate
