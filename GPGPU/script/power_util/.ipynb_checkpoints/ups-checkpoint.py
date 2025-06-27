import time
import csv
import subprocess
import os
import argparse
import psutil

# Constants for RAPL energy files
RAPL_PATH = "/sys/class/powercap/"
setpoint_dram_power = 0
pre_ipc = 0


def discover_dram_rapl_files():
    """Discover DRAM energy files from RAPL."""
    dram_energy_files = {}
    for socket_id in range(2):  # Assuming up to two sockets
        dram_energy_file = os.path.join(RAPL_PATH, f'intel-rapl:{socket_id}', f'intel-rapl:{socket_id}:0', 'energy_uj')
        if os.path.exists(dram_energy_file):
            dram_energy_files[f'dram_socket{socket_id}'] = dram_energy_file
    return dram_energy_files

# Initialize DRAM energy files
DRAM_FILES = discover_dram_rapl_files()

def read_dram_energy():
    """Read the DRAM energy values from RAPL."""
    total_energy = 0
    for file_path in DRAM_FILES.values():
        try:
            with open(file_path, 'r') as f:
                total_energy += int(f.read())
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except PermissionError:
            print(f"Permission denied for file {file_path}.")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return total_energy / 1_000_000  # Convert to joules

def collect_ipc():
    """Collect IPC data using `perf stat`."""
    try:
        output = subprocess.check_output(
            ['perf', 'stat', '-e', 'instructions,cycles', '-a', '--no-merge', '--field-separator=,', '-x,', 'sleep', '0.1'],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        instructions = int(next(line.split(',')[0] for line in output.splitlines() if 'instructions' in line))
        cycles = int(next(line.split(',')[0] for line in output.splitlines() if 'cycles' in line))
        ipc = instructions / cycles if cycles > 0 else None
        return ipc
    except subprocess.CalledProcessError as e:
        print(f"Error collecting IPC: {e}")
        return None


def ups(dram_power, ipc):
    global setpoint_dram_power
    global pre_ipc
    delta_dram_power = dram_power - setpoint_dram_power
    delta_ipc = ipc - pre_ipc

    # DRAM power no change
    if (abs(delta_dram_power) <= setpoint_dram_power*0.05):
        pre_ipc = ipc
        subprocess.run(["sudo", "/home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh", "0.8", "0.8"])

    # DRAM power increase, C- > M
    elif delta_dram_power > setpoint_dram_power * 0.05:
        setpoint_dram_power = dram_power
        subprocess.run(["sudo", "/home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh", "2.4", "0.8"])

    # DRAM power decrease
    elif delta_dram_power < -setpoint_dram_power * 0.05:
        # M -> C
        if delta_ipc >= pre_ipc * 0.05:
            setpoint_dram_power = dram_power
            pre_ipc = ipc
            subprocess.run(["sudo", "/home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh", "2.4", "0.8"])

        # performance degradation
        elif delta_ipc < -pre_ipc * 0.05:
            pre_ipc = ipc
            subprocess.run(["sudo", "/home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh", "2.4", "0.8"])
        

def monitor_dram_power_and_ipc(benchmark_pid, output_csv,interval=0.01):
    """Monitor DRAM power and IPC, store data and write to CSV after monitoring ends."""
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    power_ipc_data = []  # Store data until the loop ends

    start_time = time.time()
    initial_energy = read_dram_energy()

    while psutil.pid_exists(benchmark_pid):
        # time.sleep(interval)
        current_time = time.time() - start_time
        final_energy = read_dram_energy()
        energy_diff = final_energy - initial_energy

        # Convert energy to power (Watts)
        dram_power = energy_diff / 0.4
        initial_energy = final_energy

        ipc = collect_ipc()

        # Append data to list
        power_ipc_data.append([round(current_time, 2), dram_power, ipc])



      
        ups(dram_power,ipc)
        

    # Write all data to CSV once monitoring ends
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time (s)', 'DRAM Power (W)', 'IPC'])
        writer.writerows(power_ipc_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor DRAM power and IPC.')
    parser.add_argument('--pid', type=int, required=True, help='PID of the benchmark process')
    parser.add_argument('--output_csv', type=str, required=True, help='Output CSV file path')
    # parser.add_argument('--ups', type=int, required=True)
    args = parser.parse_args()
    monitor_dram_power_and_ipc(args.pid, args.output_csv)
    

