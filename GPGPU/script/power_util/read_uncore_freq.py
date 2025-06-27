import time
import csv
import argparse
import subprocess
import psutil
import os

# Function to read uncore frequency for a specific core
def read_uncore_frequency(core):
    try:
        # Read the Model-Specific Register (MSR) value for the uncore frequency
        msr_value = subprocess.check_output(['sudo', 'rdmsr', '-p', str(core), '0x621']).strip().decode('utf-8')
        
        # Extract the lower 8 bits to get the frequency ratio
        frequency_ratio = int(msr_value, 16) & 0xFF
        
        # Convert the ratio to GHz
        frequency_ghz = frequency_ratio * 100 / 1000
        
        return frequency_ghz
    except subprocess.CalledProcessError as e:
        print(f"Error reading MSR for core {core}: {e}")
        return 0.0

# Function to monitor uncore frequency
def monitor_uncore_frequency(benchmark_pid, output_csv, interval=0.1):
    start_time = time.time()
    frequency_data = []

    while psutil.pid_exists(benchmark_pid):
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        # Read uncore frequency for core 0 and core 1
        uncore_freq_core0_ghz = read_uncore_frequency(0)
        uncore_freq_core1_ghz = read_uncore_frequency(1)
        
        frequency_data.append([
            elapsed_time,
            uncore_freq_core0_ghz,
            uncore_freq_core1_ghz
        ])
    
    # Write the results to the output CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Core 0 Uncore Frequency (GHz)', 'Core 1 Uncore Frequency (GHz)'])
        writer.writerows(frequency_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor Intel CPU uncore frequency for core 0 and core 1.')
    parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
    parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
    args = parser.parse_args()

    monitor_uncore_frequency(args.pid, args.output_csv)

