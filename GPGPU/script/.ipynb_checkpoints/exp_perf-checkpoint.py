import os
import subprocess
import time
import signal
import argparse
import csv
import psutil
import threading
import tempfile

# Define paths and executables
home_dir = os.path.expanduser('~')
python_executable = subprocess.getoutput('which python3')  # Adjust based on your Python version

# scripts for CPU, GPU power monitoring
read_cpu_power = "./power_util/read_cpu_power.py"
read_gpu_power = "./power_util/read_gpu_power.py"
read_performance= "./power_util/read_performance.py"

# scritps for running various benchmarks
run_ecp = "./run_benchmark/run_ecp.py"
run_npb = "./run_benchmark/run_npb.py"
run_altis = "./run_benchmark/run_altis.py"

npb_benchmarks = ['bt','cg','ep','ft','is','lu','mg','sp','ua']
ecp_benchmarks = ['LULESH', 'XSBench_omp','RSBench_omp']


altis_benchmarks_0 = ['busspeeddownload','busspeedreadback','maxflops']
altis_benchmarks_1 = ['bfs','gemm','gups','pathfinder','sort']
altis_benchmarks_2 = ['cfd','cfd_double','fdtd2d','kmeans','lavamd',
                      'nw','particlefilter_float','particlefilter_naive','raytracing',
                      'srad','where']


altis_benchmarks_0 = []
altis_benchmarks_1 = []
altis_benchmarks_2 = ['fdtd2d']

cpu_caps = [70, 90, 110, 130, 150, 170, 190, 210, 230, 250]

# Setup environment
modprobe_command = "sudo modprobe msr"
sysctl_command = "sudo sysctl -n kernel.perf_event_paranoid=-1"
pm_command = "sudo nvidia-smi -i 0 -pm ENABLED"

subprocess.run(modprobe_command, shell=True)
subprocess.run(sysctl_command, shell=True)
subprocess.run(pm_command, shell=True)


def run_benchmark(benchmark_script_dir, benchmark, suite, test):
    def cap_exp(cpu_cap):  
        if suite == "ecp":
            run_benchmark_command = f"{python_executable} {run_ecp} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"
        elif suite == "npb":
            run_benchmark_command = f"{python_executable} {run_npb} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"
        else:
            run_benchmark_command = f"{python_executable} {run_altis} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"

        start = time.time()
        ipc_values = []

        # Create a temporary file to store the perf output
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Start the benchmark process
        benchmark_process = subprocess.Popen(run_benchmark_command, shell=True)

        # Start the perf process and redirect the output to the temp file
        perf_command = ['perf', 'stat', '-I', '200', '-e', 'instructions,cycles', '-a']
        with open(temp_file_path, 'w') as temp_file:
            perf_process = subprocess.Popen(perf_command, stdout=temp_file, stderr=temp_file, text=True)

        # Wait for the benchmark process to finish
        benchmark_process.wait()

        # Terminate the perf process after the benchmark ends
        perf_process.terminate()
        perf_process.wait()
        
        # Post-process the temporary file to extract IPC values
        with open(temp_file_path, 'r') as temp_file:
            for line in temp_file:
                if "insn per cycle" in line:
                    parts = line.split()
                    # The IPC value should be in the 4th position after splitting by spaces
                    try:
                        ipc = float(parts[-4])
                        ipc_values.append(ipc)
                    except ValueError:
                        print(f"Skipping invalid IPC value: {parts[-4]}")

        # Clean up the temporary file
        os.remove(temp_file_path)

        # Write IPC values to CSV
        csv_filename = f"/home/cc/power/data/cpu_performance/{suite}/ipc_{benchmark}_{cpu_cap}.csv"
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        
        with open(csv_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time (s)', 'IPC'])
            for i, ipc in enumerate(ipc_values):
                writer.writerow([i * 0.2, ipc])  # Assuming 1-second intervals for simplicity
    
        end = time.time()
        runtime = end - start
        print(f"Benchmark {benchmark} completed in {runtime:.2f} seconds")

    # Run the experiment for the given CPU cap
    cap_exp(540)  # Replace with actual `cpu_cap` values or logic as needed


if __name__ == "__main__":
   # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run benchmarks and monitor power consumption.')
    parser.add_argument('--benchmark', type=str, help='Optional name of the benchmark to run', default=None)
    parser.add_argument('--test', type=int, help='whether it is a test run', default=None)
    parser.add_argument('--suite', type=int, help='0 for ECP, 1 for ALTIS, 2 for NPB, 3 for all', default=1)
    parser.add_argument('--benchmark_size', type=int, help='0 for big, 1 for small', default=0)

    args = parser.parse_args()
    benchmark = args.benchmark
    test = args.test
    suite = args.suite
    benchmark_size = args.benchmark_size

    if suite == 0 or suite == 3:
        benchmark_script_dir = f"/home/cc/power/script/run_benchmark/ecp_script"
        # single test
        if benchmark:
            run_benchmark(benchmark_script_dir, benchmark, "ecp", test)
        # run all ecp benchmarks
        else:
            for benchmark in ecp_benchmarks:
                run_benchmark(benchmark_script_dir, benchmark, "ecp", test)
    
    if suite == 2 or suite == 3:
        benchmark_script_dir = f"/home/cc/power/script/run_benchmark/npb_script/big/"
        if benchmark_size == 1:
            benchmark_script_dir = f"/home/cc/power/script/run_benchmark/npb_script/small/"
        if benchmark:
            run_benchmark(benchmark_script_dir, benchmark, "npb", test)
        # run all npb benchmarks
        else:
            for benchmark in npb_benchmarks:
                run_benchmark(benchmark_script_dir, benchmark, "npb", test)

    if suite == 1 or suite ==3:
        # Map of benchmarks to their paths
        benchmark_paths = {
            "level0": altis_benchmarks_0,
            "level1": altis_benchmarks_1,
            "level2": altis_benchmarks_2
        }
    
        if benchmark:
            # Find which level the input benchmark belongs to
            found = False
            for level, benchmarks in benchmark_paths.items():
                if benchmark in benchmarks:
                    benchmark_script_dir = f"power/script/run_benchmark/altis_script/{level}"
                    run_benchmark(benchmark_script_dir, benchmark,"altis",test)
                    found = True
                    break
        else:
    
            for benchmark in altis_benchmarks_0:
                benchmark_script_dir = "power/script/run_benchmark/altis_script/level0"
                run_benchmark(benchmark_script_dir, benchmark,"altis",test)
            
            
            for benchmark in altis_benchmarks_1:
                benchmark_script_dir = "power/script/run_benchmark/altis_script/level1"
                run_benchmark(benchmark_script_dir, benchmark,"altis",test)
            
            
            for benchmark in altis_benchmarks_2:
                benchmark_script_dir = "power/script/run_benchmark/altis_script/level2"
                run_benchmark(benchmark_script_dir, benchmark,"altis",test)



