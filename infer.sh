#!/bin/bash

# Check if the required arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <image_name>"
    exit 1
fi

# Store the value of pkl_path argument
img="$1"

# Run the Python script with the provided pkl_name argument
python infer.py --input "figs/${img}.jpg"
