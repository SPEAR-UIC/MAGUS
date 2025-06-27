#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/altis/build/bin/level1"

"$benchmark_dir/gemm" -s 1 --passes 5000