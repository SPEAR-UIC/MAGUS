cmake_minimum_required(VERSION 3.8)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
# Set CUDA compiler
set(CMAKE_CUDA_COMPILER "/usr/local/cuda/bin/nvcc")
project(Altis LANGUAGES CXX CUDA)

add_subdirectory(src)
