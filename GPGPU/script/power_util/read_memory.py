import time
import os
import csv
import argparse
import psutil
import subprocess  
import pandas as pd



script_dir = "/home/cc/power/tools/pcm/build/bin/pcm-memory"


# Function to monitor power consumption of all GPUs
def monitor_memory_throughput():
    
    monitor_command_memory = f"echo 9900 | sudo -S {script_dir} 1"
    monitor_process_memory = subprocess.Popen(monitor_command_memory, shell=True, stdin=subprocess.PIPE, text=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read memory throughput')
    parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
    parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
    args = parser.parse_args()

    
    monitor_memory_throughput()



