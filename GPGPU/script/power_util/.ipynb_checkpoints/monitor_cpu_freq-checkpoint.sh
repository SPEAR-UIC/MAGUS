#!/bin/bash

# CSV file to store the frequencies after termination
CSV_FILE="cpu_frequencies.csv"

# Write the header to the CSV file
header="Time"
for CPU_ID in {0..7}; do
    header+=",cpu$CPU_ID"
done

# Initialize an array to store data rows
declare -a data_array
data_array+=("$header")

# Function to collect frequencies
collect_frequencies() {
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local row="$timestamp"

    for CPU_ID in {0..7}; do
        # Check if the CPU ID directory exists
        if [ -d "/sys/devices/system/cpu/cpu$CPU_ID/cpufreq" ]; then
            # Read the current frequency for the specified CPU core
            FREQUENCY=$(cat /sys/devices/system/cpu/cpu$CPU_ID/cpufreq/scaling_cur_freq)

            # Convert frequency to GHz with proper decimal places and leading 0
            FREQUENCY_GHZ=$(echo "scale=2; $FREQUENCY / 1000000" | bc | awk '{printf "%.2f", $0}')
            
            # Append the frequency to the row
            row+=",${FREQUENCY_GHZ}"
        else
            # If the CPU does not exist or does not support frequency scaling, append 'N/A'
            row+=",N/A"
        fi
    done

    # Store the row in the array instead of writing to the file
    data_array+=("$row")
}

# Function to write the collected data to the CSV file
write_to_csv() {
    echo "Writing collected data to $CSV_FILE..."
    for row in "${data_array[@]}"; do
        echo "$row" >> "$CSV_FILE"
    done
    echo "Data successfully written to $CSV_FILE."
}

# Trap SIGINT (Ctrl+C) and SIGTERM to write data to the CSV before exiting
trap 'write_to_csv; exit' SIGINT SIGTERM

# Infinite loop to collect the data every 0.5 seconds
while true; do
    collect_frequencies
    
done
