#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/altis/build/bin/level2"

"$benchmark_dir/raytracing" --passes 5 -s 2
