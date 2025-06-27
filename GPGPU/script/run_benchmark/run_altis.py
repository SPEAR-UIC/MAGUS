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
    print(benchmark,benchmark_script_dir)
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
