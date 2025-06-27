import argparse
import os
import subprocess
import sys

# Parse command-line arguments for a specific benchmark
parser = argparse.ArgumentParser(description='Run specific benchmark.')
parser.add_argument('--benchmark', type=str, help='Name of the benchmark to run', required=True)
parser.add_argument('--benchmark_script_dir', type=str, help='script directory of the benchmark', required=True)
args = parser.parse_args()

# Function to run the specified benchmark
def run(benchmark, benchmark_script_dir):
    # Construct the path to the script based on provided arguments
    print(benchmark)
    script_path = os.path.join(benchmark_script_dir, f"{benchmark}.sh")

    # Check if the script exists
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} does not exist.")
        sys.exit(1)

    # Change directory to the script's directory to ensure relative paths work
    os.chdir(os.path.dirname(script_path))

    # Execute the script
    try:
        subprocess.run(['bash', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the benchmark: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run(args.benchmark, args.benchmark_script_dir)







# Function to run the specified benchmark
# def run_benchmark(benchmark):
#     # home_directory = os.path.expanduser('~')  # Get user's home directory
#     home_directory = args.home_dir
#     # Define commands for your benchmarks
#     benchmarks = {
#         'LULESH': f"cd {os.path.join(home_directory, './benchmark/LULESH', './')} && ./lulesh2.0 -s 40",
#         'miniFE': f"cd {os.path.join(home_directory, './benchmark/miniFE', 'ref/src')} && ./miniFE.x -nx 128 -ny 128 -nz 128",
#         'Nekbone': f"cd {os.path.join(home_directory, './benchmark/Nekbone', 'test/example1')} && ./nekbone",
#         'AMG2013': f"cd {os.path.join(home_directory, './benchmark/AMG2013', 'test')} && mpirun -n 8 amg2013 -pooldist 1 -r 12 12 12",
#         'FT':      f"cd {os.path.join(home_directory, './benchmark/NPB3.4.2/NPB3.4-OMP', 'bin')} && ./ft.C.x",
#         'CG':      f"cd {os.path.join(home_directory, './benchmark/NPB3.4.2/NPB3.4-OMP', 'bin')} && ./cg.C.x",
#         'MG':      f"cd {os.path.join(home_directory, './benchmark/NPB3.4.2/NPB3.4-OMP', 'bin')} && ./mg.C.x",
#     }

#     benchmark_command = benchmarks.get(args.benchmark)
#     if benchmark_command:
#         print(f"Running {args.benchmark} benchmark...")
#         subprocess.run(benchmark_command, shell=True, check=True)
#         print(f"{args.benchmark} benchmark completed.")
#     else:
#         print(f"Benchmark {args.benchmark} is not defined.")
