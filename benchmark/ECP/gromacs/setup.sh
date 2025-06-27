#!/bin/bash

export PATH=/snap/bin:$PATH
export GMX_GPU_DD_COMMS=true
export GMX_GPU_PME_PP_COMMS=true
export GMX_FORCE_UPDATE_DEFAULT_GPU=true
export OMP_NUM_THREADS=64  

cd ./build
cmake .. -DGMX_MPI=ON -DGMX_BUILD_OWN_FFTW=ON -DGMX_GPU=CUDA -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda
make -j$(nproc)



cd ./workdir
export PATH=$HOME/benchmark/ECP/gromacs/build/bin:$PATH
echo "1" | gmx_mpi pdb2gmx -f 1UBQ.pdb -o conf.gro -p topol.top -water spce -ignh
gmx_mpi editconf -f conf.gro -o boxed.gro -c -d 10.0 -bt cubic
gmx_mpi solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top
gmx_mpi grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr -maxwarn 1
echo "SOL" | gmx_mpi genion -s ions.tpr -o solvated_ions.gro -p topol.top -pname NA -nname CL -neutral -np 500 -nn 500

gmx_mpi grompp -f em.mdp -c solvated_ions.gro -p topol.top -o em.tpr

# # Step 1: Run energy minimization (on CPU)
# echo "Running energy minimization on CPU"
# mpirun -np 1 gmx_mpi mdrun -v -deffnm em -nb cpu

# # Step 2: Generate input for MD run
# echo "Generating input for MD run"
# mpirun -np 1 gmx_mpi grompp -f md.mdp -c em.gro -p topol.top -o md.tpr
