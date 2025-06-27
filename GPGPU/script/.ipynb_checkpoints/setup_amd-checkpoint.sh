#!/bin/bash

# Step 1: Clone the repositories
cd /home/cc
git clone https://github.com/amd/esmi_ib_library.git
git clone https://github.com/amd/amd_energy.git
git clone https://github.com/amd/amd_hsmp.git

sudo apt-get update
sudo apt-get --assume-yes install cmake
sudo apt-get --assume-yes install libhwloc15 libhwloc-dev libjansson4 libjansson-dev

# Step 2: Build and install amd_energy
cd amd_energy
make
sudo make modules_install
sudo modprobe amd_energy
sudo insmod ./amd_energy.ko
cd ..

# Step 3: Build and install amd_hsmp
cd amd_hsmp
make
sudo make modules_install
sudo modprobe amd_hsmp
sudo insmod ./amd_hsmp.ko
cd ..

sed -i '11s|#include <asm/amd_hsmp.h>|#include "/home/cc/amd_hsmp/amd_hsmp.h"|' esmi_ib_library/include/e_smi/e_smi.h

# Step 5: Modify e_smi_monitor.h to include the correct path to amd_hsmp.h
sed -i '19s|#include <asm/amd_hsmp.h>|#include "/home/cc/amd_hsmp/amd_hsmp.h"|' esmi_ib_library/include/e_smi/e_smi_monitor.h



# Step 5: Build and install esmi_ib_library
cd esmi_ib_library
mkdir -p build
cd build
cmake ../
cmake -DENABLE_STATIC_LIB=1 ../
make
sudo make install

echo "AMD eSMI library setup completed successfully!"
