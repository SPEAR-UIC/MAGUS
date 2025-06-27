#!/bin/bash

# Check if at least one CPU ID is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <CPU_IDs>"
    echo "Example: $0 0 1 2"
    exit 1
fi

# Iterate over each CPU ID and print the current frequency
for CPU_ID in "$@"; do
    # Check if the CPU ID directory exists
    if [ -d "/sys/devices/system/cpu/cpu$CPU_ID/cpufreq" ]; then
        # Read the current frequency for the specified CPU core
        FREQUENCY=$(cat /sys/devices/system/cpu/cpu$CPU_ID/cpufreq/scaling_cur_freq)
        
        # Convert frequency to GHz with proper decimal places and leading 0
        FREQUENCY_GHZ=$(echo "scale=2; $FREQUENCY / 1000000" | bc | awk '{printf "%.2f", $0}')
        echo "CPU $CPU_ID frequency: $FREQUENCY_GHZ GHz"
    else
        echo "CPU $CPU_ID does not exist or does not support frequency scaling."
    fi
done