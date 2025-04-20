#!/bin/bash
set -e  # Exit on error
echo "Starting model download process..."
mkdir -p model/ || { echo "Failed to create model/ directory"; exit 1; }
echo "Installing gdown..."
pip install --upgrade gdown || { echo "Failed to install gdown"; exit 1; }
echo "Downloading model files from Google Drive..."
for i in {1..3}; do
    gdown --folder https://drive.google.com/drive/folders/1TDffvXwAn8sl6QIqLX7OjbUvFAYmdXkU -O model/ --remaining-ok && break
    echo "Download attempt $i failed. Retrying in $((2**i)) seconds..."
    sleep $((2**i))
done
if [ ! -f model/config.json ]; then
    echo "Failed to download config.json after 3 attempts"
    exit 1
fi
echo "Model files downloaded successfully"
ls -l model/ || { echo "Failed to list model/ directory"; exit 1; }