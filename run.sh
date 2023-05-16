#!/bin/bash

# Install necessary system packages (Termux-specific)
pkg install python-numpy -y
pkg install libjpeg-turbo -y
pkg install x11-repo firefox geckodriver
pkg install python-cryptography

# Check if the required packages are installed
python scripts/check_requirements.py requirements.txt
if [ $? -eq 1 ]; then
    echo Installing missing packages...
    pip install -r requirements.txt
fi

# Run the autogpt module
python -m autogpt "$@"

# Wait for user input before exiting
read -p "Press any key to continue..."

