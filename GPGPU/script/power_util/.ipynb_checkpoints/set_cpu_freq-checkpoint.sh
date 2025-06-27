#!/bin/bash

# Check if at least two arguments are provided (CPU IDs and frequency)
if [ $# -lt 2 ]; then
    echo "Usage: $0 <CPU_IDs> <FREQUENCY>"
    echo "Example: $0 0 1 2.3"
    exit 1
fi

# Extract the last argument as the frequency in GHz
FREQUENCY_GHZ=${@: -1}

# Convert the frequency to a format that cpufreq-set understands (e.g., 2.3GHz)
FREQUENCY="${FREQUENCY_GHZ}GHz"

# Extract all but the last argument as CPU IDs
CPU_IDS=${@:1:$#-1}

# Iterate over each CPU ID and apply the settings
for CPU_ID in $CPU_IDS; do
    # Set the governor to userspace for the specified CPU core
    # sudo cpufreq-set -c $CPU_ID -g userspace
    
    # Set the maximum frequency for the specified CPU core using cpufreq-set
    sudo cpufreq-set -c $CPU_ID -u $FREQUENCY  # Set the maximum frequency

    echo "CPU $CPU_ID maximum frequency set to $FREQUENCY"
done
