#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <model_checkpoint> <file_name>"
    exit 1
fi

# Assigning parameters to variables
model_checkpoint="$1"
image_file="$2"

# Execute the provided command
python inference.py --pth "$model_checkpoint" --img_glob "preprocessed/${image_file}_aligned_rgb.png" --output_dir "inferred/" --visualize --no_cuda
