#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/sw4lite/optimize_cuda"

cd ${benchmark_dir}

./sw4lite ../tests/pointsource/ps2.in


# mpirun -n 8 sw4lite ../tests/cartesian/uni.in
#mpirun -n 8 sw4lite ../tests/topo/gaussianHill.in
# mpirun -n 16 sw4lite ../tests/pointsource/pointsource.in