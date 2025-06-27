#!/bin/bash

nvidia-smi --query-gpu=index,timestamp,power.draw,clocks.sm,clocks.mem --format=csv -l 1