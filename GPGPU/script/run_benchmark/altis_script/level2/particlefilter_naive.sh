#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/altis/build/bin/level2"

"$benchmark_dir/particlefilter_naive" --passes 1 -s 4
