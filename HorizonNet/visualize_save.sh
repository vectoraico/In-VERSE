#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <image_file> [extra parameters]"
    exit 1
fi

# Assigning parameters to variables
img="$1"
extra_params="${@:2}"  # Collect all extra parameters

# Execute the provided command
python layout_viewer.py --img "preprocessed/${img}_aligned_rgb.png" --layout "inferred/${img}_aligned_rgb.json" --vis --out "../In-VERSE/static/models/output/${img}" $extra_params

# Extra params
# --out, usage: --out output/out.ply
