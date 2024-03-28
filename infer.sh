#!/bin/bash

# Check if the required arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <img_glob>"
    exit 1
fi

# Store the value of img_glob argument
img_glob="$1"

#pip install numpy==1.21.0 -qq
pip install numpy==1.21.0 -qq 2>/dev/null

# Execute the Python command
python inference.py --cfg src/config/mp3d.yaml --img_glob "$img_glob" --output_dir src/output --post_processing manhattan

#python inference.py --cfg src/config/other/horizon_net_mp3d.yaml --img_glob "$img_glob" --output_dir src/output --post_processing manhattan
