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



setup_pcm() {
    cd "./src/"
    mkdir build
    cd build
    cmake ..
    cmake --build . --parallel
    sudo modprobe msr
}

setup_benchmark() {
    cd "./benchmark/"
    sudo ./setup.sh
}

install_dependence
setup_pcm
setup_benchmark
