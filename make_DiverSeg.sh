#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 SRC_DIR DST_DIR FILE_LIST"
    exit 1
fi

SRC_DIR="$1"
DST_DIR="$2"
FILE_LIST="$3"

# Read the file list line by line
while IFS= read -r TARGET_PATH
do
    # The file path in SRC_DIR
    SRC_FILE="$SRC_DIR/$TARGET_PATH"

    # The file path in DST_DIR
    DST_FILE="$DST_DIR/$TARGET_PATH"

    # Create the directory if it does not exist
    DST_DIR_PATH=$(dirname "$DST_FILE")
    mkdir -p "$DST_DIR_PATH"
    
    # Copy the file
    if [ -f "$SRC_FILE" ]; then
        cp "$SRC_FILE" "$DST_FILE"
    else
        echo "File $SRC_FILE does not exist"
    fi
done < "$FILE_LIST"
