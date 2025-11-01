
## Setup environment
./setup.sh

## Start MAGUS as a background process with sudo 
sudo ./src/build/bin/pcm-memory 0.1 --uncore_0 0.8 --uncore_1 0.8 --dynamic_ufs_mem 1 --inc_ts 300
--dec_ts 500 --history 5 --burst_up 0.4 &


## Run application for example
./raytracing --passes 1 -s 4


## Cite Our Work
Zhong Zheng, Seyfal Sultanov, Michael E. Papka, and Zhiling Lan. 2025. Minimizing Power Waste in Heterogenous Computing via Adaptive Uncore
Scaling. In The International Conference for High Performance Computing,
Networking, Storage and Analysis (SC ’25), November 16–21, 2025, St Louis,
MO, USA. ACM, New York, NY, USA, 14 pages. https://doi.org/10.1145/3712285.3759879
