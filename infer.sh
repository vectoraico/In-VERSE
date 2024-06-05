#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file_name>"
    exit 1
fi

# Assigning parameters to variables
image_file="$1"

# Execute the provided command
python HorizonNet/inference.py --pth HorizonNet/ckpt/resnet50_rnn__mp3d.pth --img_glob "HorizonNet/preprocessed/${image_file}_aligned_rgb.png" --output_dir "HorizonNet/inferred/" --visualize --no_cuda
