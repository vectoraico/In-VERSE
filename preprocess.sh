#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <image_file> [extra parameters]"
    exit 1
fi

# Assigning parameters to variables
img_glob="$1"
extra_params="${@:2}"  # Collect all extra parameters

# Execute the provided command
python HorizonNet/preprocess.py --img_glob "HorizonNet/assets/$img_glob" --output_dir "HorizonNet/preprocessed/" $extra_params


# Extra params
# --refine_iter, default=3
# --q_error, default=0.7
