#!/bin/bash

# Check if the required arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pkl_name>"
    exit 1
fi

# Store the value of pkl_path argument
pkl_name="$1"

# Install numpy version 1.24.4
pip install numpy==1.24.4

# Run the Python script with the provided pkl_name argument
python 3d.py --pkl_path "src/output/pkl/$pkl_name"
