#!/bin/bash


# Convert cap from Watts to microWatts and apply it

cap_uw=$(($1 * 500000))  # Convert W to uW


#Apply the cap to both sockets
echo $cap_uw | sudo tee /sys/class/powercap/intel-rapl:0/constraint_0_power_limit_uw
echo $cap_uw | sudo tee /sys/class/powercap/intel-rapl:1/constraint_0_power_limit_uw
echo $cap_uw | sudo tee /sys/class/powercap/intel-rapl:0/constraint_1_power_limit_uw
echo $cap_uw | sudo tee /sys/class/powercap/intel-rapl:1/constraint_1_power_limit_uw


