#!/bin/bash

# Build script for WeatherApp
# Creates a standalone executable using PyInstaller

set -e  # Exit on error

echo "Installing PyInstaller..."
pip install pyinstaller

echo "Building WeatherApp executable..."

# Determine the platform-specific separator for --add-data
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    SEPARATOR=";"
else
    # macOS and Linux
    SEPARATOR=":"
fi

# Build the executable
pyinstaller \
    --onefile \
    --windowed \
    --name weatherapp \
    --hidden-import tkinter \
    --add-data ".env.example${SEPARATOR}." \
    src/weatherapp/__main__.py

echo "Build complete!"
echo "The executable can be found in the 'dist' directory."
echo ""
echo "Note: You need to create a .env file with your API key in the same directory as the executable."
echo "You can copy .env.example to .env and fill in your WEATHER_API_KEY."
