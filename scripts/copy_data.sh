#!/usr/bin/env bash

#script for copying over data downloaded from old script to new script format

dataset=validation

for full in backupdata/$dataset/compressedmusicxml/*mxl; do
    filename=$(basename "$full")
    file="${filename%.*}"
    mkdir -p "data/$dataset/$file"
    mv "$full" "data/$dataset/$file"
done
