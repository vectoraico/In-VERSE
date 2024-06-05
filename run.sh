#!/bin/bash

# Check if the argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 filename"
  exit 1
fi

# Get the full filename and the base name without the extension
FILENAME=$1
BASENAME=$(basename "$FILENAME" .jpg) # assuming the extension is always .jpg

# Call the scripts with appropriate arguments
./preprocess.sh "$FILENAME"
./infer.sh "$BASENAME"
./visualize_save.sh "$BASENAME"
