#!/bin/bash

# Define source and destination directories
source_directory="./"
destination_directory="../"

# Loop through the files in the source directory
for file in "${source_directory}/"inputs_*; do
  # Extract the number from the file name
  number=$(echo "${file}" | sed -n 's/.*inputs_\([0-9]*\)\.npy/\1/p')

  # Check if the number is less than 50
  if [ "${number}" -lt 20 ]; then
    # Move both inputs and labels files
    mv "${source_directory}/inputs_${number}.npy" "${destination_directory}/"
    mv "${source_directory}/labels_${number}.npy" "${destination_directory}/"
  fi
done

