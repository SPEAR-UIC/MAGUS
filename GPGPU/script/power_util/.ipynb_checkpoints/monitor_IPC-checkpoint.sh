#!/bin/bash

# CSV file to store the IPC data after termination
CSV_FILE="cpu_ipc.csv"

# Write the header to the CSV file if it doesn't exist
if [ ! -f "$CSV_FILE" ]; then
    echo "Time,IPC" > "$CSV_FILE"
fi

# Function to collect IPC data
collect_ipc() {
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    output=$(perf stat -e instructions,cycles -a --no-merge --field-separator=',' -x, sleep 0.1 2>&1)
    instructions=$(echo "$output" | grep instructions | awk -F',' '{print $1}')
    cycles=$(echo "$output" | grep cycles | awk -F',' '{print $1}')
    if [ "$cycles" -ne 0 ]; then
        ipc=$(echo "scale=2; $instructions / $cycles" | bc)
    else
        ipc="N/A"
    fi
    echo "$timestamp,$ipc" >> "$CSV_FILE"
}

# Trap SIGINT (Ctrl+C) and SIGTERM to exit gracefully
trap 'exit' SIGINT SIGTERM

# Infinite loop to collect the data every 0.5 seconds
while true; do
    collect_ipc
done
