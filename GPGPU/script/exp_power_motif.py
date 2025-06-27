import os
import subprocess
import time
import signal
import argparse
import psutil


# Define paths and executables
home_dir = os.path.expanduser('~')
python_executable = subprocess.getoutput('which python3')  # Adjust based on your Python version

# scripts for CPU, GPU power monitoring
read_cpu_power = "./power_util/read_cpu_power.py"
read_gpu_power = "./power_util/read_gpu_power.py"
reda_dram_power = "./power_util/read_dram_power.py"
ups_script = "./power_util/ups"
read_uncore_frequency = "./power_util/read_uncore_freq.py"
# read_memory = "./power_util/read_memory_throughput.py"

# scritps for running various benchmarks
run_altis = "./run_benchmark/run_altis.py"
run_ecp = "./run_benchmark/run_ecp.py"
run_npb = "./run_benchmark/run_npb.py"

read_memory = "/home/cc/power/tools/pcm/build/bin/pcm-memory"


## parameters passed into pcm-memory
gpu_power_ts = 70
pcm = 0
uncore_0 = 0.8
uncore_1 = 0.8
dynamic_ufs_mem = 0
dynamic_ufs_gpuP = 1
inc_ts = 0
dec_ts = 0
history=2
dual_cap = 0
burst_up=0.4
burst_low=0.2
power_shift=0
g_cap = 0
ups = 0
SoC = 0
memory_throughput_ts = 40000;


# Define your benchmarks, for testing replace the list with just ['FT'] for example
# ecp_benchmarks = ['FT', 'CG', 'LULESH', 'Nekbone', 'AMG2013', 'miniFE']

npb_benchmarks = ['bt','cg','ep','ft','is','lu','mg','sp','ua']

altis_benchmarks_0 = ['busspeeddownload','busspeedreadback','maxflops']
altis_benchmarks_1 = ['bfs','gemm','gups','pathfinder','sort']
altis_benchmarks_2 = ['cfd','cfd_double','fdtd2d','kmeans','lavamd',
                      'nw','particlefilter_float','particlefilter_naive','raytracing',
                      'srad','where']

ecp_benchmarks = ['miniGAN','CRADL','sw4lite','Laghos', 'lammps', 'UNet', 'Resnet50','bert_large','gromacs']

# ecp_benchmarks = ['miniGAN','CRADL','sw4lite','Laghos','UNet']

# Setup environment
modprobe_command = "sudo modprobe msr"
sysctl_command = "sudo sysctl -n kernel.perf_event_paranoid=-1"
pm_command = "sudo nvidia-smi -i 0 -pm ENABLED"

subprocess.run(modprobe_command, shell=True)
subprocess.run(sysctl_command, shell=True)
subprocess.run(pm_command, shell=True)




def run_benchmark(benchmark_script_dir,benchmark, suite, test):
    
    if g_cap==0 and power_shift==0:
        tmp="/no_power_shift/"
    elif g_cap==1 and power_shift==0:
        tmp="/cap/noShift/"
    elif g_cap==1 and power_shift ==1:
        tmp="/cap/shift/"
    if ups:
        ups_tag = "_ups"
    else:
        ups_tag = ""
    if SoC:
        SoC_tag = "_SoC"
    else:
        SoC_tag = ""
    if not test:
        output_cpu = f"../data/{suite}_power_res/{tmp}{benchmark}_power_cpu{ups_tag}{SoC_tag}.csv"
        output_gpu = f"../data/{suite}_power_res/{tmp}{benchmark}_power_gpu{ups_tag}{SoC_tag}.csv"
        output_uncore = f"../data/{suite}_power_res/{tmp}uncore_freq/{benchmark}_uncore_freq{ups_tag}{SoC_tag}.csv"
    else:
        output_cpu = f"../data/{suite}_test/{benchmark}_power_cpu.csv"
        output_gpu = f"../data/{suite}_test/{benchmark}_power_gpu.csv"
        output_uncore = f"../data/{suite}_test/{benchmark}_uncore_freq.csv"

    
################################## PCM Memory Monitoring Starts ##############################

    if pcm:
        # start pcm-memory
        monitor_command_memory = f"echo 9900 | sudo -S {read_memory} 0.1 --suite {suite} --benchmark {benchmark} --uncore_0 {uncore_0} --uncore_1 {uncore_1} --dynamic_ufs_mem {dynamic_ufs_mem} --inc_ts {inc_ts} --dec_ts {dec_ts} --history {history} --dual_cap {dual_cap} --burst_up {burst_up} --burst_low {burst_low} --power_shift {power_shift} --g_cap {g_cap} --ups {ups} --memory_throughput_ts {memory_throughput_ts}"
        monitor_process_memory = subprocess.Popen(monitor_command_memory, shell=True, stdin=subprocess.PIPE, text=True)


################################## PCM Memory Monitoring Ends ##############################


    

################################## Benchmarking Starts ##############################
    
    # Execute the benchmark and get its PID
    if suite == "altis":
        run_benchmark_command = f" {python_executable} {run_altis} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"

    elif suite == "ecp":
        run_benchmark_command = f" {python_executable} {run_ecp} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"

    elif suite == "npb":
        run_benchmark_command = f"{python_executable} {run_npb} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"
        
    start = time.time()
    benchmark_process = subprocess.Popen(run_benchmark_command, shell=True)
    benchmark_pid = benchmark_process.pid


################################## Benchmarking Ends ##############################


################ UPS starts ###############

    # # if ups==1:
    # output_ups_dram_ipc =  f"../data/{suite}_power_res/{tmp}{benchmark}_dram_ipc{ups_tag}.csv"
    # ups_command = f"echo 9900 | sudo -S taskset -c 158 {python_executable} {ups_script} --output_csv {output_ups_dram_ipc} --pid {benchmark_pid} --ups {ups}"
    # monitor_process = subprocess.Popen(ups_command, shell=True, stdin=subprocess.PIPE, text=True)

    if ups == 1:
        output_ups_dram_ipc = f"../data/{suite}_power_res/{tmp}{benchmark}_dram_ipc{ups_tag}.csv"

        ups_command = f"echo 9900 | sudo -S ./power_util/ups --output_csv={output_ups_dram_ipc} --pid={benchmark_pid} --dual_cap={dual_cap}"
        monitor_process = subprocess.Popen(ups_command, shell=True, stdin=subprocess.PIPE, text=True)


################ UPS ends ###############


################ SoC starts ###############

    if SoC == 1:
        output_SoC_cpu_util = f"../data/{suite}_power_res/{tmp}{benchmark}_cpu_util{SoC_tag}.csv"

        SoC_command = f"echo 9900 | sudo -S ./power_util/SoC/SoC --output_csv={output_SoC_cpu_util} --pid={benchmark_pid} --dual_cap={dual_cap}"
        monitor_process = subprocess.Popen(SoC_command, shell=True, stdin=subprocess.PIPE, text=True)


################ SoC ends ###############



################################## CPU & GPU Power and Frequency Monitoring Starts ##############################

    # Start CPU power monitoring, passing the PID of the benchmark process
    monitor_command_cpu = f"echo 9900 | sudo -S  {python_executable} {read_cpu_power}  --output_csv {output_cpu} --pid {benchmark_pid}"
    monitor_process = subprocess.Popen(monitor_command_cpu, shell=True, stdin=subprocess.PIPE, text=True)
    
    if suite == "altis" or suite == "ecp": 
        # Start GPU power monitoring, passing the PID of the benchmark process
        monitor_command_gpu = f"echo 9900 | sudo -S  {python_executable} {read_gpu_power}  --output_csv {output_gpu} --pid {benchmark_pid} --dynamic_uncore {dynamic_ufs_gpuP} --gpu_power_ts {gpu_power_ts}"
        monitor_process = subprocess.Popen(monitor_command_gpu, shell=True, stdin=subprocess.PIPE, text=True)

    
    # start CPU uncore frequency monitoring
    monitor_command_cpu = f"echo 9900 | sudo -S {python_executable} {read_uncore_frequency}  --output_csv {output_uncore} --pid {benchmark_pid}"
    monitor_process = subprocess.Popen(monitor_command_cpu, shell=True, stdin=subprocess.PIPE, text=True)



################################## CPU & GPU Power and Frequency Monitoring Ends ##############################






################################## Finalization Starts ##############################

    # Wait for the benchmark process to complete
    benchmark_exit_code = benchmark_process.wait()


    if pcm:
        # kill pcm-memory
        if monitor_process_memory.poll() is None:  # Check if it's still running
            parent_pid = monitor_process_memory.pid
                # Get the parent process
            parent = psutil.Process(parent_pid)
            # Find and kill child processes
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.terminate()  # Or child.kill() for a forceful kill
                except:
                    pass


    end = time.time()
    runtime = end - start
    print("Runtime: ",runtime)
    if benchmark_exit_code != 0:
        print(f"Benchmark {benchmark} failed")
    else:
        print(f"Completed benchmark: {benchmark}")


            
################################## Finalization Ends ##############################
    


if __name__ == "__main__":

################################## Parsing Args Starts ##############################
    
   # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run benchmarks and monitor power consumption.')
    parser.add_argument('--benchmark', type=str, help='Optional name of the benchmark to run', default=None)
    parser.add_argument('--test', type=int, help='whether it is a test run', default=None)
    parser.add_argument('--suite', type=int, help='0 for ECP, 1 for ALTIS, 2 for NPB, 3 for all', default=1)
    parser.add_argument('--benchmark_size', type=int, help='0 for big, 1 for small', default=0)
    parser.add_argument('--uncore_0', type=float, default=2.4)
    parser.add_argument('--uncore_1', type=float, default=2.4)
    parser.add_argument('--dynamic_ufs_gpuP', type=int, help='0 for no, 1 for yes', default=0)
    parser.add_argument('--pcm', type=int, help='0 for no, 1 for yes', default=0)
    parser.add_argument('--dynamic_ufs_mem', type=int, help='0 for no, 1 for yes', default=0)
    parser.add_argument('--inc_ts', type=int, default=0)
    parser.add_argument('--dec_ts', type=int, default=0)
    parser.add_argument('--history', type=int, default=2)
    parser.add_argument('--dual_cap', type=int, default=1)
    parser.add_argument('--burst_up', type=float, default=0.4)
    parser.add_argument('--burst_low', type=float, default=0.2)
    parser.add_argument('--power_shift', type=int, default=0)
    parser.add_argument('--g_cap', type=int, default=0)
    parser.add_argument('--ups', type=int, default=0)
    parser.add_argument('--SoC', type=int, default=0)
    parser.add_argument('--memory_throughput_ts', type=int, default=60000)
    


    args = parser.parse_args()
    benchmark = args.benchmark
 
    test = args.test
    suite = args.suite
    benchmark_size = args.benchmark_size
    dynamic_ufs_gpuP = args.dynamic_ufs_gpuP
    dynamic_ufs_mem = args.dynamic_ufs_mem
    pcm = args.pcm
    uncore_0 = args.uncore_0
    uncore_1 = args.uncore_1
    inc_ts = args.inc_ts
    dec_ts = args.dec_ts
    history = args.history
    dual_cap = args.dual_cap
    power_shift=args.power_shift
    g_cap = args.g_cap
    ups = args.ups
    memory_throughput_ts = args.memory_throughput_ts
    SoC = args.SoC

################################## Parsing Args Ends ##############################



    
################################## Initialization Starts ##############################
    

    script_dir = "/home/cc/power/GPGPU/script/power_util/"

    # if not args.dynamic_uncore_fs:
    # set initial uncore frequency
    subprocess.run([script_dir + "/set_uncore_freq.sh", str(args.uncore_0), str(args.uncore_1)]) 

################################## Initialization Ends ##############################




################################## Run Benchmark Starts ##############################
    
    if suite == 0 or suite ==3:
        benchmark_script_dir = f"power/GPGPU/script/run_benchmark/ecp_script"
        # single test
        if benchmark:
            run_benchmark(benchmark_script_dir, benchmark,"ecp",test)
        # run all ecp benchmarks
        else:
            for benchmark in ecp_benchmarks:
                run_benchmark(benchmark_script_dir, benchmark,"ecp",test)
    

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
                    benchmark_script_dir = f"power/GPGPU/script/run_benchmark/altis_script/{level}"
                    run_benchmark(benchmark_script_dir, benchmark,"altis",test)
                    found = True
                    break
        else:
    
            for benchmark in altis_benchmarks_0:
                benchmark_script_dir = "power/GPGPU/script/run_benchmark/altis_script/level0"
                run_benchmark(benchmark_script_dir, benchmark,"altis",test)
            
            
            for benchmark in altis_benchmarks_1:
                benchmark_script_dir = "power/GPGPU/script/run_benchmark/altis_script/level1"
                run_benchmark(benchmark_script_dir, benchmark,"altis",test)
            
            
            for benchmark in altis_benchmarks_2:
                benchmark_script_dir = "power/GPGPU/script/run_benchmark/altis_script/level2"
                run_benchmark(benchmark_script_dir, benchmark,"altis",test)


    if suite == 2 or suite == 3:
        benchmark_script_dir = f"power/GPGPU/script/run_benchmark/npb_script/big/"
        if benchmark_size ==1:
            benchmark_script_dir = f"power/GPGPU/script/run_benchmark/npb_script/small/"
        
        # single test
        if benchmark:
            run_benchmark(benchmark_script_dir, benchmark,"npb",test)
        # run all ecp benchmarks
        else:
            for benchmark in npb_benchmarks:
                run_benchmark(benchmark_script_dir, benchmark,"npb",test)
                
################################## Run Benchmark Ends ##############################

