#!/bin/bash

# Move to the working directory
cd /home/cc/benchmark/ECP/gromacs/build/workdir

# Set environment variables for GPU communication and offloading
export PATH=$HOME/benchmark/ECP/gromacs/build/bin:$PATH
export GMX_GPU_DD_COMMS=true
export GMX_GPU_PME_PP_COMMS=true
export GMX_FORCE_UPDATE_DEFAULT_GPU=true
export OMP_NUM_THREADS=64  # Optimize thread usage for MPI
# export CUDA_VISIBLE_DEVICES=0,1,2,3

# Step 1: Run energy minimization (on CPU)
echo "Running energy minimization on CPU"
mpirun -np 1 gmx_mpi mdrun -v -deffnm em -nb cpu

# Step 2: Generate input for MD run
echo "Generating input for MD run"
mpirun -np 1 gmx_mpi grompp -f md.mdp -c em.gro -p topol.top -o md.tpr

# Step 3: Run MD simulation with GPU offloading

echo "Running MD simulation with GPU offloading"

mpirun -np 1 gmx_mpi mdrun -v -deffnm md -nb gpu -pme gpu -bonded gpu -update gpu



# #!/bin/bash

# # Move to the working directory
# cd /home/cc/benchmark/ECP/gromacs/build/workdir

# # Set environment variables for GPU communication and offloading
# export PATH=$HOME/benchmark/ECP/gromacs/build/bin:$PATH
# export GMX_GPU_DD_COMMS=true
# export GMX_GPU_PME_PP_COMMS=true
# export GMX_FORCE_UPDATE_DEFAULT_GPU=true
# export OMP_NUM_THREADS=64  # Optimize thread usage for MPI
# export CUDA_VISIBLE_DEVICES=0,1,2,3

# # Step 1: Run energy minimization (on CPU)
# echo "Running energy minimization on CPU"
# mpirun -np 1 gmx_mpi mdrun -v -deffnm em -nb cpu

# # Step 2: Generate input for MD run
# echo "Generating input for MD run"
# mpirun -np 1 gmx_mpi grompp -f md.mdp -c em.gro -p topol.top -o md.tpr

# # Step 3: Run MD simulation with GPU offloading

# echo "Running MD simulation with GPU offloading"
# mpirun -np 4 gmx_mpi mdrun -v -deffnm md -nb gpu -pme gpu -bonded gpu -update gpu -gpu_id 0,1,2,3 -npme 1


