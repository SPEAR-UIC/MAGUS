#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/altis/build/bin/level0"


"$benchmark_dir/maxflops" --passes 10 -s 5
