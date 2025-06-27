# import time
# import os
# import csv
# import argparse
# import psutil

# # Constants for RAPL energy files specific to your system
# RAPL_PATH = "/sys/class/powercap/"

# def discover_rapl_sockets():
#     """Discover CPU and DRAM energy files from RAPL."""
#     energy_files = {}
    
#     # Check for CPU and DRAM energy files
#     for socket_id in range(2):  # Adjust if you have more sockets
#         cpu_energy_file = f"/sys/class/powercap/intel-rapl:{socket_id}/energy_uj"
#         dram_energy_file = f"/sys/class/powercap/intel-rapl:{socket_id}/intel-rapl:{socket_id}:0/energy_uj"
        
#         if os.path.exists(cpu_energy_file):
#             energy_files[f'cpu_socket{socket_id}'] = cpu_energy_file
#             print(f"Found CPU socket energy file: {cpu_energy_file}")

#         if os.path.exists(dram_energy_file):
#             energy_files[f'dram_socket{socket_id}'] = dram_energy_file
#             print(f"Found DRAM socket energy file: {dram_energy_file}")

#     if not energy_files:
#         print("No energy files found. Check if RAPL is enabled on your system.")
    
#     return energy_files

# # Initialize ENERGY_FILES with available sockets
# ENERGY_FILES = discover_rapl_sockets()


# def read_energy(file_path):
#     """Read the energy value from a given RAPL energy file."""
#     try:
#         with open(file_path, 'r') as f:
#             return int(f.read())
#     except FileNotFoundError:
#         print(f"File {file_path} not found.")
#         return 0
#     except PermissionError:
#         print(f"Permission denied when reading the file {file_path}.")
#         return 0
#     except Exception as e:
#         print(f"Error reading the file {file_path}: {e}")
#         return 0

# def monitor_power(benchmark_pid, output_csv, avg, interval=0.5):
#     """Monitor power consumption for CPU sockets and DRAM."""
#     start_time = time.time()
#     initial_values = {key: read_energy(path) for key, path in ENERGY_FILES.items()}
#     power_data = []
#     total_cpu_energy = 0
#     total_dram_energy = 0

#     while psutil.pid_exists(benchmark_pid):
#         time.sleep(interval)
#         current_time = time.time()
#         elapsed_time = current_time - start_time
#         current_values = {key: read_energy(path) for key, path in ENERGY_FILES.items()}



#         energy_consumed = {
#             key: (current_values[key] - initial_values[key]) / 1_000_000  # Convert to joules
#             for key in ENERGY_FILES
#         }
#         initial_values = current_values

#         # Sum energy for CPU and DRAM sockets
#         cpu_energy = sum(energy_consumed[key] for key in energy_consumed if 'cpu_socket' in key)
#         dram_energy = sum(energy_consumed[key] for key in energy_consumed if 'dram_socket' in key)

        
#         total_cpu_energy += cpu_energy
#         total_dram_energy += dram_energy

#         # Convert energy to power (Watts)
#         cpu_power = cpu_energy / interval
#         dram_power = dram_energy / interval

#         power_data.append([elapsed_time, cpu_power, dram_power])

#     os.makedirs(os.path.dirname(output_csv), exist_ok=True)

#     if avg:
#         file_exists = os.path.isfile(output_csv)
#         with open(output_csv, 'a', newline='') as file:
#             writer = csv.writer(file)
#             if not file_exists:
#                 writer.writerow(['CPU_E (J)', 'DRAM_E (J)'])
#             writer.writerow([round(total_cpu_energy, 2), round(total_dram_energy, 2)])
#     else:
#         with open(output_csv, 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Time (s)', 'Package Power (W)', 'DRAM Power (W)'])
#             writer.writerows(power_data)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Monitor power usage using RAPL for all CPU sockets and DRAM.')
#     parser.add_argument('--pid', type=int, required=True, help='PID of the benchmark process')
#     parser.add_argument('--output_csv', type=str, required=True, help='Output CSV file path')
#     parser.add_argument('--avg', type=int, default=0, help='Collect average energy (1 for True, 0 for False)')
#     args = parser.parse_args()

#     monitor_power(args.pid, args.output_csv, args.avg)


import time
import os
import csv
import argparse
import psutil

# Constants for RAPL energy files specific to your system
RAPL_PATH = "/sys/class/powercap/"
def discover_rapl_sockets():
    rapl_path = "/sys/class/powercap/"
    energy_files = {}
    # Check and add energy files for existing sockets
    for socket_id in range(2):  # Assuming a maximum of two sockets for this example
        cpu_energy_file = os.path.join(rapl_path, f'intel-rapl:{socket_id}', 'energy_uj')
        if os.path.exists(cpu_energy_file):
            energy_files[f'cpu_socket{socket_id}'] = cpu_energy_file
    return energy_files

# Initialize ENERGY_FILES with available sockets
ENERGY_FILES = discover_rapl_sockets()


def read_energy(file_path):
    try:
        with open(file_path, 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return 0
    except PermissionError:
        print(f"Permission denied when reading the file {file_path}.")
        return 0
    except Exception as e:
        print(f"Error reading the file {file_path}: {e}")
        return 0
    
# Function to monitor power consumption updated to add socket powers together
def monitor_power(benchmark_pid, output_csv, avg, interval=0.1):
    start_time = time.time()
    initial_values = {key: read_energy(os.path.join(RAPL_PATH, path)) for key, path in ENERGY_FILES.items()}
    power_data = []
    tot = 0
    while psutil.pid_exists(benchmark_pid):
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time
        current_values = {key: read_energy(os.path.join(RAPL_PATH, path)) for key, path in ENERGY_FILES.items()}

        energy_consumed = {key: (current_values[key] - initial_values[key]) / 1_000_000 for key in ENERGY_FILES}  # Convert microjoules to joules
        initial_values = current_values

        # Sum the energy for the CPU sockets
        total_cpu_energy = sum(energy_consumed[key] for key in energy_consumed if 'cpu_socket' in key)
        tot += total_cpu_energy
        # Calculate individual power for DRAM or any other component if necessary
        # total_dram_energy = sum(energy_consumed[key] for key in energy_consumed if 'dram_socket' in key)
        # Convert energy to power
        cpu_power = total_cpu_energy / interval
        # dram_power = total_dram_energy / interval

        power_data.append([elapsed_time, cpu_power])

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    if avg:
        file_exists = os.path.isfile(output_csv)
        with open(output_csv, 'a', newline='') as file:  # Open file in append mode
            writer = csv.writer(file)
            if not file_exists:  # If the file doesn't exist, add the header
                writer.writerow(['CPU_E (J)'])
            writer.writerow([round(tot,2)])  # Append the total energy
    else:
        with open(output_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time (s)', 'Package Power (W)'])
            writer.writerows(power_data)

# Main function and argument parsing remains the same

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor total power usage using RAPL for all CPU sockets and DRAM.')
    parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
    parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
    parser.add_argument('--avg', type=str, help='avg_power', default=0)
    args = parser.parse_args()

    monitor_power(args.pid, args.output_csv,args.avg)


# import os
# import time
# import csv
# import psutil
# import subprocess
# import argparse

# # Function to read the socket power using e_smi_tool
# def read_socket_power():
#     try:
#         result = subprocess.run(['sudo', '/home/cc/esmi_ib_library/build/e_smi_tool', '--showsockpower'], capture_output=True, text=True)
#         output = result.stdout

#         # The rest of the parsing logic
#         for line in output.splitlines():
#             if "Power (Watts)" in line:
#                 parts = line.split('|')
#                 if len(parts) >= 4:
#                     power_socket_0 = float(parts[2].strip())
#                     power_socket_1 = float(parts[3].strip())
#                     return [power_socket_0, power_socket_1]
#                 else:
#                     raise ValueError("Unexpected format in power line: " + line)

#         raise ValueError("Failed to parse power values from e_smi_tool output.")

#     except subprocess.CalledProcessError as e:
#         print(f"Error executing e_smi_tool: {e}")
#         return [0, 0]
#     except Exception as e:
#         print(f"Error reading socket power: {e}")
#         return [0, 0]


# # Function to monitor power consumption updated to add socket powers together
# def monitor_power(benchmark_pid, output_csv, avg, interval=0.2):
#     start_time = time.time()
#     power_data = []
#     total_energy = 0
    
#     while psutil.pid_exists(benchmark_pid):
#         time.sleep(interval)
#         current_time = time.time()
#         elapsed_time = current_time - start_time
        
#         power_values = read_socket_power()
#         total_cpu_power = sum(power_values)
#         total_energy += total_cpu_power * interval
        
#         power_data.append([elapsed_time, total_cpu_power])
    
#     os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
#     if avg:
#         with open(output_csv, 'a', newline='') as file:
#             writer = csv.writer(file)
#             if os.stat(output_csv).st_size == 0:  # If the file is empty, add the header
#                 writer.writerow(['CPU_E (J)'])
#             writer.writerow([round(total_energy, 2)])  # Append the total energy
#     else:
#         with open(output_csv, 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Time (s)', 'Package Power (W)'])
#             writer.writerows(power_data)

# # Main function and argument parsing
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Monitor total power usage using e_smi_tool for all CPU sockets.')
#     parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
#     parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
#     parser.add_argument('--avg', type=str, help='avg_power', default=0)
#     args = parser.parse_args()

#     monitor_power(args.pid, args.output_csv, args.avg)





