#!/bin/bash
set -e  # Exit on error
echo "Downloading model files from Google Drive..."
pip install gdown || { echo "Failed to install gdown"; exit 1; }
gdown --folder https://drive.google.com/drive/folders/1TDffvXwAn8sl6QIqLX7OjbUvFAYmdXkU?usp=sharing -O model/ || { echo "Failed to download model files"; exit 1; }
echo "Model files downloaded successfully"
ls -l model/  # List downloaded files for debugging