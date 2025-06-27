#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/lammps/build/"

cd ${benchmark_dir}
# export OMP_NUM_THREADS=1


# mpirun -np 1 lmp -sf gpu -pk gpu 1 -in ../input/in.lj

# mpirun -np 1 lmp -sf gpu -pk gpu 1 -in ../bench/POTENTIALS/in.meam

mpirun -np 1 lmp -sf gpu -pk gpu 1 -in ../input/in.lj 

# mpirun -np 4 lmp -sf gpu -pk gpu 4 -in ../input/in.lj 