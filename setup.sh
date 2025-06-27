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
    sudo pip install scikit-learn
    sudo pip install scipy
    sudo pip install plotly
    sudo pip install faiss-cpu
    sudo pip install seaborn
    sudo pip install kaggle
    sudo pip install tensorflow
    sudo pip install tensorly
    sudo pip install networkx
    sudo apt install git-lfs
    sudo git lfs install


}

generate_altis_data() {
    cd "./benchmark/altis/data/kmeans"
    python3 datagen.py -n 8388608 -f
    python3 datagen.py -n 1048576 -f

    
}

setup_miniGAN_env() {
    cd "./benchmark/ECP/miniGAN/data"
    python3 generate_bird_images.py --dim-mode 3 --num-images 2048 --image-dim 64 --num-channels 3

    cd "./benchmark/ECP/miniGAN/"

    bash ./setup_python_env.sh
}

setup_CRADL() {
    cd "./benchmark/ECP/CRADL/"
    python3 -m venv CRADL_env
    source CRADL_env/bin/activate
    bash INSTALL
    deactivate
    # cd ./data
    # bash ./filter.sh

}

setup_UNet() {
    cd "./benchmark/ECP/UNet/"
    python3 -m venv UNet_env
    source UNet_env/bin/activate
    pip install -r requirements.txt
    deactivate
    bash scripts/download_data.sh
    python3 shrink_dataset.py
}

setup_Resnet() {
    cd "./benchmark/ECP/Resnet50/"
    ./setup.sh
    
}

setup_bert() {
    cd "./benchmark/ECP/bert/"
    source /home/cc/benchmark/ECP/UNet/UNet_env/bin/activate
    ./download_data.sh
    deactivate
}



setup_lammps() {
    cd "./benchmark/ECP/lammps/build"
    bash ./setup.sh
}

setup_gromacs() {
    cd "./benchmark/ECP/gromacs"
    bash ./setup.sh
}

setup_Laghos() {
    cd "./benchmark/ECP/hypre-2.11.2/src/"
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


setup_pcm() {
    cd "./src/"
    mkdir build
    cd build
    cmake ..
    cmake --build . --parallel
    sudo modprobe msr
}

setup_altis() {
    cd "./benchmark/altis"
    sudo ./setup.sh
}

install_dependence
setup_pcm
setup_altis
generate_altis_data
setup_Laghos
setup_CRADL
setup_RSBench
setup_lammps
setup_gromacs
setup_UNet
setup_Resnet
setup_miniGAN_env
setup_docker
