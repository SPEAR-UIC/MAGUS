#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <FREQUENCY_GHz_CPU0> <FREQUENCY_GHz_CPU1>"
    echo "Example: $0 2.2 1.8"
    exit 1
fi

# Assign the arguments to variables
FREQUENCY_GHZ_CPU0=$1
FREQUENCY_GHZ_CPU1=$2

# Function to validate the frequency and calculate the hexadecimal ratio
calculate_ratio() {
    local FREQUENCY_GHZ=$1
    # Check if the frequency is within the allowed range (0.8 GHz to 2.4 GHz)
    if (( $(echo "$FREQUENCY_GHZ < 0.8" | bc -l) )) || (( $(echo "$FREQUENCY_GHZ > 2.4" | bc -l) )); then
        echo "Error: Frequency must be between 0.8 GHz and 2.4 GHz"
        exit 1
    fi
    # Calculate the ratio (frequency in GHz * 10)
    local RATIO=$(echo "$FREQUENCY_GHZ * 10" | bc | awk '{printf "%d\n", $1}')
    # Convert the ratio to hexadecimal
    printf '%02X' $RATIO
}

# Calculate ratios for both CPU 0 and CPU 1
RATIO_HEX_CPU0=$(calculate_ratio $FREQUENCY_GHZ_CPU0)
RATIO_HEX_CPU1=$(calculate_ratio $FREQUENCY_GHZ_CPU1)

# Combine the ratio for min and max (min=max) for each CPU
COMBINED_HEX_CPU0="0x${RATIO_HEX_CPU0}${RATIO_HEX_CPU0}"
COMBINED_HEX_CPU1="0x${RATIO_HEX_CPU1}${RATIO_HEX_CPU1}"

# Write to MSR 0x620 for both CPU 0 and CPU 1
sudo wrmsr -p 0 0x620 $COMBINED_HEX_CPU0
sudo wrmsr -p 1 0x620 $COMBINED_HEX_CPU1

# echo "Set uncore frequency to $FREQUENCY_GHZ_CPU0 GHz (Hex: $COMBINED_HEX_CPU0) for CPU 0"
# echo "Set uncore frequency to $FREQUENCY_GHZ_CPU1 GHz (Hex: $COMBINED_HEX_CPU1) for CPU 1"

