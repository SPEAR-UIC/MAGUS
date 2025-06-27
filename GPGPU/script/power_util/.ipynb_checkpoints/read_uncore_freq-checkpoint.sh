#!/bin/bash

# Function to read and convert the uncore frequency
read_uncore_frequency() {
    local core=$1
    local msr_value=$(sudo rdmsr -p $core 0x621)
    
    # Print the raw MSR value
    echo "Core $core: Raw MSR Value = $msr_value"
    
    # Use Python to extract the lower 8 bits and convert the ratio
    local frequency_ratio=$(python3 -c "print(int('$msr_value', 16) & 0xFF)")
    
    # Print the extracted frequency ratio
    echo "Core $core: Extracted Frequency Ratio = $frequency_ratio"
    
    # Calculate the actual uncore frequency in MHz and GHz
    local frequency_mhz=$((frequency_ratio * 100))
    local frequency_ghz=$(echo "scale=2; $frequency_mhz / 1000" | bc)
    
    echo "Core $core: Uncore Frequency = $frequency_mhz MHz ($frequency_ghz GHz)"
}

# Read and convert the uncore frequency for each specified core
for core in "$@"; do
    read_uncore_frequency $core
done
