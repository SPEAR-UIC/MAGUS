import time
import os
import csv
import argparse
import psutil
import subprocess  
import pandas as pd



high_uncore_freq = 1
gpu_power_ts = 100
script_dir = "/home/cc/power/GPGPU/script/power_util/"
dynamic_uncore = 0

def scale_uncore_freq(gpu_powers):
    global high_uncore_freq
  
    for p in gpu_powers:
        
        # Scale up: set uncore frequency to 2.4 GHz
        if p <= gpu_power_ts and high_uncore_freq == 0:
            subprocess.run([script_dir + "/set_uncore_freq.sh", "2.4", "2.4"], check=True)
            high_uncore_freq = 1
        # Scale down: set uncore frequency to 0.8 GHz
        elif p > gpu_power_ts and high_uncore_freq == 1:
            subprocess.run([script_dir + "/set_uncore_freq.sh", "0.8", "0.8"], check=True)
            high_uncore_freq = 0

def get_gpu_power():
    # Run the nvidia-smi command to get power usage for all GPUs, parse it
    smi_output = subprocess.check_output(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'], encoding='utf-8')
    # Split the output by lines, convert each one from string to float
    power_draws = [float(power_draw.strip()) for power_draw in smi_output.strip().split('\n')]
    return power_draws

# Function to monitor power consumption of all GPUs
def monitor_gpu_power(benchmark_pid, output_csv, avg, interval=0.1):
    start_time = time.time()
    power_data = []

    while psutil.pid_exists(benchmark_pid):
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time

        gpu_powers = get_gpu_power()

        if dynamic_uncore:
            scale_uncore_freq(gpu_powers)
        
        
        row = [elapsed_time] + gpu_powers
        power_data.append(row)

    # subprocess.run([script_dir + "/set_uncore_freq.sh", "2.4"], check=True)
    # os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    if avg:
        file_exists = os.path.isfile(output_csv)
        total_time = power_data[-1][0]  # Total elapsed time is the time value in the last row
        # Calculate average power for all GPUs and then total energy
        avg_power_all_gpus = sum([sum(p[i] for p in power_data) / len(power_data) for i in range(1, len(gpu_powers) + 1)])
        total_energy = round(avg_power_all_gpus * total_time,2)  # Total energy for all GPUs
    
        with open(output_csv, 'a', newline='') as file:  # Open file in append mode
            writer = csv.writer(file)
            if not file_exists:  # If the file doesn't exist, add the header
                writer.writerow(['GPU_E (J)'])
            writer.writerow([total_energy])  # Append the total energy

            
    else:   
        with open(output_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            # Adjust the header based on the number of GPUs
            headers = ['Time (s)'] + [f'GPU {i} Power (W)' for i in range(len(gpu_powers))]
            writer.writerow(headers)
            writer.writerows(power_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor GPU power usage using nvidia-smi.')
    parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
    parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
    parser.add_argument('--avg', type=str, help='avg_power', default=0)
    parser.add_argument('--dynamic_uncore_frequency', type=int, help='enable dynamic uncore frequency scaling', default=0)
    parser.add_argument('--gpu_power_ts', type=int, help='gpu power threshold', default=70)
    args = parser.parse_args()
    dynamic_uncore = args.dynamic_uncore_frequency
    monitor_gpu_power(args.pid, args.output_csv, args.avg)


# import time
# import os
# import csv
# import argparse
# import psutil
# import subprocess  
# import pandas as pd

# # Global variables for uncore frequency scaling
# high_uncore_freq = 1
# script_dir = "/home/cc/power/GPGPU/script/power_util/"
# dynamic_uncore = 0

# def scale_uncore_freq(sm_clocks):
#     """Scale the uncore frequency based on GPU clocks."""
#     global high_uncore_freq

#     for clock in sm_clocks:
#         # Scale up: set uncore frequency to 2.4 GHz if clocks are below threshold
#         if clock <= args.gpu_power_ts and high_uncore_freq == 0:
#             subprocess.run([os.path.join(script_dir, "set_uncore_freq.sh"), "2.4", "2.4"], check=True)
#             high_uncore_freq = 1
#         # Scale down: set uncore frequency to 0.8 GHz if clocks are above threshold
#         elif clock > args.gpu_power_ts and high_uncore_freq == 1:
#             subprocess.run([os.path.join(script_dir, "set_uncore_freq.sh"), "0.8", "0.8"], check=True)
#             high_uncore_freq = 0

# def get_gpu_clocks():
#     """Fetch the current SM and memory clocks using nvidia-smi."""
#     try:
#         smi_output = subprocess.check_output(
#             ["nvidia-smi", "--query-gpu=clocks.sm,clocks.mem", "--format=csv,noheader,nounits"],
#             encoding='utf-8'
#         )
#         # Split the output into SM and memory clocks for all GPUs
#         clocks = [line.split(", ") for line in smi_output.strip().split("\n")]
#         return [(int(sm_clock), int(mem_clock)) for sm_clock, mem_clock in clocks]
#     except Exception as e:
#         print(f"Error fetching GPU clocks: {e}")
#         return []

# def monitor_gpu_clocks(benchmark_pid, output_csv, avg, interval=0.1):
#     """Monitor the GPU clocks over time."""
#     start_time = time.time()
#     clock_data = []

#     while psutil.pid_exists(benchmark_pid):
#         time.sleep(interval)
#         current_time = time.time()
#         elapsed_time = current_time - start_time

#         gpu_clocks = get_gpu_clocks()  # Get SM and memory clocks for all GPUs

#         if dynamic_uncore:
#             scale_uncore_freq([sm_clock for sm_clock, _ in gpu_clocks])

#         # Create a row with elapsed time and the clock readings for each GPU
#         row = [elapsed_time] + [value for clocks in gpu_clocks for value in clocks]
#         clock_data.append(row)

#     if avg:
#         file_exists = os.path.isfile(output_csv)
#         total_time = clock_data[-1][0]  # Total elapsed time

#         # Calculate the average of all SM and memory clocks
#         avg_clocks = [
#             sum([row[i] for row in clock_data]) / len(clock_data)
#             for i in range(1, len(clock_data[0]))
#         ]

#         with open(output_csv, 'a', newline='') as file:
#             writer = csv.writer(file)
#             if not file_exists:
#                 headers = ['Avg SM Clock (MHz)', 'Avg Mem Clock (MHz)']
#                 writer.writerow(headers)
#             writer.writerow([round(clock, 2) for clock in avg_clocks])
#     else:
#         with open(output_csv, 'w', newline='') as file:
#             writer = csv.writer(file)
#             headers = ['Time (s)'] + [f'GPU {i} SM Clock (MHz)' for i in range(len(gpu_clocks))] + \
#                       [f'GPU {i} Mem Clock (MHz)' for i in range(len(gpu_clocks))]
#             writer.writerow(headers)
#             writer.writerows(clock_data)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Monitor GPU clocks using nvidia-smi.')
#     parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
#     parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
#     parser.add_argument('--avg', type=int, help='Calculate average clocks', default=0)
#     parser.add_argument('--dynamic_uncore_frequency', type=int, help='Enable dynamic uncore frequency scaling', default=0)
#     parser.add_argument('--gpu_power_ts', type=int, help='GPU clock threshold for uncore scaling', default=1000)
#     args = parser.parse_args()

#     dynamic_uncore = args.dynamic_uncore_frequency
#     monitor_gpu_clocks(args.pid, args.output_csv, args.avg)

