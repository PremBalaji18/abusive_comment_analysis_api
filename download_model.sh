#!/bin/bash
set -e  # Exit on error
echo "Starting model download process..."
mkdir -p model/ || { echo "Failed to create model/ directory"; exit 1; }
echo "Installing gdown..."
pip install --upgrade gdown || { echo "Failed to install gdown"; exit 1; }
echo "Downloading model files from Google Drive..."
gdown --folder https://drive.google.com/drive/folders/1TDffvXwAn8sl6QIqLX7OjbUvFAYmdXkU -O model/ --remaining-ok || { echo "Failed to download model files"; exit 1; }
echo "Model files downloaded successfully"
ls -l model/ || { echo "Failed to list model/ directory"; exit 1; }