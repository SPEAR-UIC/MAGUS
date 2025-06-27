#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/miniGAN/"

cd ${benchmark_dir}
source minigan_env/bin/activate
cd pytorch
python minigan_driver.py  --epoch 3 --dataset bird --num-images 2048 --num-channels 3 --image-dim 64 --dim-mode 3

#python minigan_driver.py --num-threads 40 --epoch 10 --dataset bird
deactivate