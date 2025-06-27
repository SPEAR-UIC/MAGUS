#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/altis/build/bin/level2"

"$benchmark_dir/particlefilter_float" --passes 4 -s 4
