#!/bin/bash

home_dir="/home/cc"



install_dependence() {
    sudo apt-get update
    sudo apt-get --assume-yes install gfortran
    sudo apt-get --assume-yes install openmpi-bin openmpi-common libopenmpi-dev
    sudo apt-get --assume-yes install libjpeg-dev
    sudo apt-get install -y libnccl2 libnccl-dev
    sudo apt-get install -y openmpi-bin openmpi-common libopenmpi-dev
    sudo apt --assume-yes install linux-tools-common linux-tools-$(uname -r)
    sudo snap install cmake --classic
    sudo apt-get install unzip
    sudo apt install sysstat 

    # sudo apt install linux-intel-iotg-tools-common
    # sudo apt install --assume-yes linux-tools-5.15.0-92-generic
    sudo apt-get --assume-yes install mpich
    sudo apt --assume-yes install cmake
    sudo apt --assume-yes install python3-pip
    sudo pip install psutil
    sudo apt-get --assume-yes install liblapack-dev
    sudo pip install jupyterlab
    sudo pip install numpy matplotlib pandas
    sudo pip install scipy
    sudo pip install plotly
    sudo pip install kaggle
    sudo pip install tensorflow
    sudo apt install git-lfs
    sudo git lfs install


}

setup_rapl() {
    cd "${home_dir}/power/tools/RAPL"
    make clean
    make
}

# download_rodinia_data(){
#     cd "${home_dir}"
#     wget https://dl.dropbox.com/s/cc6cozpboht3mtu/rodinia-3.1-data.tar.gz
#     tar -xzf rodinia-3.1-data.tar.gz
#     cd rodinia-data
#     mv * "${home_dir}/benchmark/rodinia/data"

# }


setup_pcm() {
    # cd "${home_dir}/power/tools"
    # git clone --recursive https://github.com/zzheng33/pcm.git
    cd "${home_dir}/power/tools/pcm"
    mkdir build
    cd build
    cmake ..
    cmake --build . --parallel
    sudo modprobe msr
}

load_benchmark() {
    cd "${home_dir}"
    git lfs install
    git clone https://github.com/zzheng33/benchmark.git
}

# setup_rodinia() {
#     cd "${home_dir}/benchmark/rodinia"
#     sudo make
# }

setup_altis() {
    cd "${home_dir}/benchmark/altis"
    sudo ./setup.sh
}

# setup_other_benchmark() {
#     # Define other benchmark setup steps here
# }

generate_altis_data() {
    cd "${home_dir}/benchmark/altis/data/kmeans"
    python3 datagen.py -n 8388608 -f
    python3 datagen.py -n 1048576 -f

    
}

setup_miniGAN_env() {
    cd "${home_dir}/benchmark/ECP/miniGAN/data"
    python3 generate_bird_images.py --dim-mode 3 --num-images 2048 --image-dim 64 --num-channels 3

    cd "${home_dir}/benchmark/ECP/miniGAN/"

    bash ./setup_python_env.sh
}

setup_CRADL() {
    cd "${home_dir}/benchmark/ECP/CRADL/"
    python3 -m venv CRADL_env
    source CRADL_env/bin/activate
    bash INSTALL
    deactivate
    # cd ./data
    # bash ./filter.sh

}

setup_UNet() {
    cd "${home_dir}/benchmark/ECP/UNet/"
    python3 -m venv UNet_env
    source UNet_env/bin/activate
    pip install -r requirements.txt
    deactivate
    bash scripts/download_data.sh
    python3 shrink_dataset.py
}

setup_Resnet() {
    cd "${home_dir}/benchmark/ECP/Resnet50/"
    ./setup.sh
    
}

setup_bert() {
    cd "${home_dir}/benchmark/ECP/bert/"
    source /home/cc/benchmark/ECP/UNet/UNet_env/bin/activate
    ./download_data.sh
    deactivate
}


setup_XSBench() {
     cd "${home_dir}/benchmark/ECP/XSBench/cuda"
     make
     cd "${home_dir}/benchmark/ECP/XSBench/openmp-threading"
  
     make
}

setup_RSBench() {
     cd "${home_dir}/benchmark/ECP/RSBench/cuda"
     make
     cd "${home_dir}/benchmark/ECP/RSBench/openmp-threading"
     make
}

setup_lammps() {
    cd "${home_dir}/benchmark/ECP/lammps/build"
    bash ./setup.sh
}

setup_gromacs() {
    cd "${home_dir}/benchmark/ECP/gromacs"
    bash ./setup.sh
}

setup_Laghos() {
    cd "${home_dir}/benchmark/ECP/hypre-2.11.2/src/"
    ./configure --with-cuda --with-gpu-arch="80" --disable-fortran
    make -j
    cd ../..
    ln -s hypre-2.11.2 hypre

    cd metis-4.0.3/
    make
    cd ..
    ln -s metis-4.0.3 metis-4.0

    cd mfem/
    make pcuda CUDA_ARCH=sm_80 -j
    cd ..

    cd Laghos/
    make -j 
    

}

setup_ecp_cpu() {
    cd "${home_dir}/benchmark/ECP/miniFE/openmp/src/"
    
    make

    cd "${home_dir}/benchmark/ECP/AMG2013/"
  
    make
}

setup_npb() {
    cd "${home_dir}/benchmark/NPB/NPB3.4-OMP/"
    
    make suite

}

setup_cpu_freq() {
    sudo apt-get update
    sudo apt-get --assume-yes install msr-tools
    sudo apt --assume-yes install cpufrequtils
    sudo modprobe cpufreq_stats
    sudo modprobe cpufreq_userspace
    sudo modprobe cpufreq_powersave
    sudo modprobe cpufreq_conservative
    sudo modprobe cpufreq_ondemand
    sudo modprobe msr


}

setup_docker() {
    # Install prerequisites
    sudo apt-get -y install ca-certificates curl gnupg lsb-release
    
    # Add Docker’s official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Set up the Docker stable repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Update package index and install Docker
    sudo apt-get -y update
    sudo apt-get -y install docker-ce docker-ce-cli containerd.io
    
    # Install NVIDIA Docker 2
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
       && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
       && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    
    # Update package index and install nvidia-docker2
    sudo apt-get -y update
    sudo apt-get -y install nvidia-docker2
    
    # Restart Docker to apply changes
    sudo systemctl restart docker
    
    # Pull the TensorFlow Docker image with GPU support
    sudo docker pull tensorflow/tensorflow:2.4.0-gpu



    
}

## need to revise to update new images
# new_image() {
#     # Start the container, keep it running with bash or sleep to allow the commit process
#     sudo docker run --gpus all -it --rm --name mlperf  -v /home/cc/benchmark/ECP/bert-large/:/workspace ten
# sorflow/tensorflow:2.4.0-gpu bash  
#     cd ./workspace/logging
#     pip install -e .
#     exec bash"  # Keep container running by opening bash

#     # Fork a new process to commit the container
#     sudo docker commit bert_c bert

#     # After committing, stop and remove the container
#     sudo docker stop bert_c
#     sudo docker rm bert_c
# }


# setup_pcm

install_dependence
load_benchmark
setup_altis
setup_pcm
generate_altis_data
setup_CRADL
setup_Laghos
setup_XSBench
setup_RSBench
setup_lammps
setup_gromacs
# setup_ecp_cpu
setup_npb
setup_cpu_freq
setup_UNet
setup_Resnet
setup_miniGAN_env
setup_docker
# new_image
