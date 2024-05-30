#!/bin/bash

# Function to install Python dependencies
install_python_dependencies() {
    # Check if pip3 is available, otherwise fall back to pip
    if command -v pip3 &>/dev/null; then
        echo "Using pip3 to install dependencies..."
        pip3 install pyttsx3
        pip3 install -r requirements.txt
    elif command -v pip &>/dev/null; then
        echo "pip3 not found, using pip to install dependencies..."
        pip install pyttsx3
        pip install -r requirements.txt
    else
        echo "pip or pip3 not found. Please install pip or pip3 and re-run this script."
        exit 1
    fi
}

# Update package lists
sudo apt-get update

# Install espeak
sudo apt-get install -y espeak

# Check Python version
python_version=$(python3 --version 2>&1)
if [[ $python_version == *"Python 3"* ]]; then
    echo "Python 3 is installed: $python_version"
    install_python_dependencies
else
    echo "Python 3 is not installed. Please install Python 3 and re-run this script."
    exit 1
fi

echo "Setup complete. You can now run your Python script."
