#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/Laghos/"

cd ${benchmark_dir}

./laghos -p 3 -m data/box01_hex.mesh -rs 1 -tf 5.0 -pa -cgt 1e-12 -d cuda