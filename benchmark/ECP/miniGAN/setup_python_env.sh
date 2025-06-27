# Run on machines/testbeds with no root privs in ${MINIGAN_ROOT}
 
PIP=pip3
PYT=python3

#${PIP} install --upgrade pip --user



${PYT} -m venv minigan_env

source minigan_env/bin/activate
export HOROVOD_CUDA_HOME=/usr/local/cuda
export HOROVOD_GPU_OPERATIONS=NCCL
export HOROVOD_MPI_HOME=/usr/lib/x86_64-linux-gnu/openmpi


${PIP} install wheel
${PIP} install torchvision==0.14
HOROVOD_CUDA_HOME=/usr/local/cuda HOROVOD_GPU_OPERATIONS=NCCL HOROVOD_MPI_HOME=/usr/lib/x86_64-linux-gnu/openmpi pip install --no-cache-dir horovod[pytorch]
${PIP} install tensorboard
${PIP} install matplotlib
${PIP} install "numpy<2"
deactivate
