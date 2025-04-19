#!/bin/bash
echo "Downloading model files from Google Drive..."

# Install gdown (Google Drive downloader)
pip install gdown

# Replace with your Google Drive folder ID
gdown --folder https://drive.google.com/drive/folders/1TDffvXwAn8sl6QIqLX7OjbUvFAYmdXkU?usp=sharing -O model/