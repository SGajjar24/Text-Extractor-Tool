#!/bin/bash

# Installation script for Text Extractor tool

echo "Installing Text Extractor tool..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Install the package
echo "Installing Text Extractor package..."
pip3 install -e .

echo "Installation complete!"
echo "You can now use the Text Extractor tool with the command: text-extractor"
echo "For more information, see the documentation in the docs/ directory."
