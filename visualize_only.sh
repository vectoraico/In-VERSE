#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <image_file>"
    exit 1
fi

# Assigning parameters to variables
img="$1"

# Execute the provided command
python visualize_only.py --img "${img}"
