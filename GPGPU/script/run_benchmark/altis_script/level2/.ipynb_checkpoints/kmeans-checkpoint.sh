#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/altis/build/bin/level2"
data_dir="${home_dir}/benchmark/altis/data/kmeans/kmeans_f_8388608_30"
# data_dir="${home_dir}/benchmark/altis/data/kmeans/kmeans_f_1048576_30"

"$benchmark_dir/kmeans" -i "$data_dir" --passes 1