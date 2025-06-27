#!/usr/bin/env bash

CC=gcc
CFLAGS="-O2 -Wall"

# Compile SoC.c into SoC.o
$CC $CFLAGS -c SoC.c -o SoC.o
if [ $? -ne 0 ]; then
    echo "Failed to compile SoC.c"
    exit 1
fi

# Compile ups.c into ups.o
$CC $CFLAGS -c ups.c -o ups.o
if [ $? -ne 0 ]; then
    echo "Failed to compile ups.c"
    exit 1
fi

# Link SoC.o and ups.o into ups executable
$CC $CFLAGS -o ups ups.o SoC.o
if [ $? -ne 0 ]; then
    echo "Failed to link ups"
    exit 1
fi

echo "Build successful: ./ups created"

# Optional: remove object files after successful build
rm -f *.o
