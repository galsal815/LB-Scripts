#!/bin/bash

generate_files() {
    local num_files=$1
    for i in $(seq 0 $(($num_files - 1))); do
        echo "Random content $RANDOM" > "${i}.txt"
    done
}

check_world_writable_files() {
    local dir=$1
    df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type f -perm -0002
}

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <number_of_files> <directory>"
    exit 1
fi

NUM_FILES=$1
DIRECTORY=$2

mkdir -p "$DIRECTORY"

cd "$DIRECTORY" || { echo "Failed to change directory to $DIRECTORY"; exit 1; }

generate_files "$NUM_FILES"

echo "Checking for world writable files..."
world_writable_files=$(check_world_writable_files "$DIRECTORY")

if [[ -z "$world_writable_files" ]]; then
    echo "No world writable files found."
else
    echo "World writable files found:"
    echo "$world_writable_files"
fi
