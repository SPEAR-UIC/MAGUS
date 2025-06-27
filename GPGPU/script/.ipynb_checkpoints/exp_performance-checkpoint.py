import os
import subprocess
import time
import signal
import argparse


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


# ecp_benchmarks = ['LULESH', 'Nekbone', 'AMG2013', 'miniFE']

npb_benchmarks = ['bt','cg','ep','ft','is','lu','mg','sp','ua']
#'miniFE'
ecp_benchmarks = ['LULESH', 'XSBench_omp','RSBench_omp']
# ecp_benchmarks = ['XSBench_omp','RSBench_omp']

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
        subprocess.run([f"./power_util/cpu_cap.sh {cpu_cap}"], shell=True)
        
        time.sleep(1)  # Wait for the power caps to take effect
        
        # Assuming other variables like python_executable, home_dir are defined elsewhere in your script
        if suite == "ecp":
            run_benchmark_command = f"{python_executable} {run_ecp} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"
        elif suite == "npb":
            run_benchmark_command = f"{python_executable} {run_npb} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"
    
        start = time.time()
        
        # Generate CSV filename including the benchmark name
        csv_filename = f"/home/cc/power/data/cpu_performance/{benchmark}/pcm_{benchmark}_{cpu_cap}.csv"
        
        pcm_process = subprocess.Popen(['sudo', '../tools/pcm/build/bin/pcm', '0.1', f'-csv={csv_filename}'],
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, 
                                       preexec_fn=os.setsid)  # Set the process group
    
        time.sleep(1.5)  # Allow some time for pcm to start and set up before starting the benchmark
        benchmark_process = subprocess.Popen(run_benchmark_command, shell=True)
    
        benchmark_process.wait()
    
        # Send SIGTERM to the entire process group to ensure pcm process is terminated
        os.killpg(os.getpgid(pcm_process.pid), signal.SIGTERM)
    
        end = time.time()
        runtime = end - start - 1.5  # Adjust runtime calculation to exclude initial sleep
        print("Runtime: ", runtime)

 
    for cpu_cap in cpu_caps:
        cap_exp(cpu_cap)

    subprocess.run([f"./power_util/cpu_cap.sh 250"], shell=True)
    subprocess.run([f"./power_util/gpu_cap.sh 260"], shell=True)




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


    if suite == 0 or suite ==3:
        benchmark_script_dir = f"/home/cc/power/script/run_benchmark/ecp_script"
        # single test
        if benchmark:
            run_benchmark(benchmark_script_dir, benchmark,"ecp",test)
        # run all ecp benchmarks
        else:
            for benchmark in ecp_benchmarks:
                run_benchmark(benchmark_script_dir, benchmark,"ecp",test)
    


    if suite == 2 or suite == 3:
        benchmark_script_dir = f"/home/cc/power/script/run_benchmark/npb_script/big/"
        if benchmark_size ==1:
            benchmark_script_dir = f"/home/cc/power/script/run_benchmark/npb_script/small/"
        if benchmark:
            run_benchmark(benchmark_script_dir, benchmark,"npb",test)
        # run all ecp benchmarks
        else:
            for benchmark in npb_benchmarks:
                run_benchmark(benchmark_script_dir, benchmark,"npb",test)






