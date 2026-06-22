# WeatherApp GUI

A simple weather application with a graphical user interface built using Python and Tkinter. Get current weather conditions and 5-day forecasts for any city worldwide.

## Features

- **Current Weather**: View temperature, weather condition, humidity, wind speed, and UV index
- **5-Day Forecast**: See upcoming weather with daily forecasts
- **Easy Search**: Simply type a city name and press Enter or click Search
- **Clean GUI**: User-friendly interface built with Tkinter

## Requirements

- Python 3.11 or higher
- Internet connection
- Free API key from [WeatherAPI.com](https://www.weatherapi.com/)

## Installation

1. **Clone or download this repository**

2. **Install the package**

   ```bash
   pip install -e .
   ```

   This will install WeatherApp along with all its dependencies:
   - requests
   - python-dotenv
   - pillow

3. **Set up your API key**

   - Sign up for a free API key at [https://www.weatherapi.com/](https://www.weatherapi.com/)
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file and add your API key:
     ```
     WEATHER_API_KEY=your_actual_api_key_here
     ```

## Usage

### Running the Application

After installation, you can run WeatherApp using the command:

```bash
weatherapp
```

Alternatively, you can run it as a Python module:

```bash
python -m weatherapp
```

### Using the GUI

1. **Search for a City**: Type a city name in the search box and press Enter or click the "Search" button
2. **View Current Weather**: The "Current" tab shows real-time weather conditions
3. **View Forecast**: Switch to the "Forecast" tab to see the 5-day weather forecast

## Building a Standalone Executable

You can create a standalone executable that doesn't require Python to be installed.

### Building on Any Platform

1. **Run the build script**:

   ```bash
   bash build.sh
   ```

   This will:
   - Install PyInstaller
   - Build a standalone executable
   - Bundle the `.env.example` file
   - Create the executable in the `dist` directory

2. **Configure the executable**:

   After building, copy `.env.example` to `.env` in the same directory as the executable and add your API key:
   ```bash
   cp .env.example dist/.env
   # Edit dist/.env and add your WEATHER_API_KEY
   ```

3. **Run the executable**:

   ```bash
   ./dist/weatherapp
   ```

### Building a macOS DMG (macOS only)

To create a distributable DMG file for macOS:

1. **First, build the executable** using the steps above:

   ```bash
   bash build.sh
   ```

2. **Create an application bundle**:

   ```bash
   # Create the app structure
   mkdir -p "WeatherApp.app/Contents/MacOS"
   mkdir -p "WeatherApp.app/Contents/Resources"
   
   # Copy the executable
   cp dist/weatherapp "WeatherApp.app/Contents/MacOS/"
   cp .env.example "WeatherApp.app/Contents/MacOS/"
   
   # Create Info.plist
   cat > "WeatherApp.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>weatherapp</string>
    <key>CFBundleIdentifier</key>
    <string>com.weatherapp.gui</string>
    <key>CFBundleName</key>
    <string>WeatherApp</string>
    <key>CFBundleVersion</key>
    <string>0.1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>0.1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
</dict>
</plist>
EOF
   ```

3. **Create the DMG**:

   ```bash
   # Create a temporary directory for DMG contents
   mkdir dmg_temp
   cp -r WeatherApp.app dmg_temp/
   
   # Copy .env.example as a reminder
   cp .env.example dmg_temp/
   
   # Create a README for users
   cat > dmg_temp/README.txt << EOF
WeatherApp Installation
=======================

1. Drag WeatherApp.app to your Applications folder
2. Copy .env.example to .env in the same directory as WeatherApp.app
3. Edit .env and add your WeatherAPI.com API key
4. Run WeatherApp from your Applications folder

Get a free API key at: https://www.weatherapi.com/
EOF
   
   # Create the DMG
   hdiutil create -volname "WeatherApp" -srcfolder dmg_temp -ov -format UDZO WeatherApp.dmg
   
   # Clean up
   rm -rf dmg_temp
   ```

4. **The DMG file `WeatherApp.dmg` is now ready for distribution!**

### Building on Windows

On Windows, after running `build.sh` (using Git Bash or similar), you can create an installer using:

- **Inno Setup**: Free installer creator for Windows
- **NSIS**: Another free Windows installer system

Or simply distribute the `dist/weatherapp.exe` file along with the `.env.example` file.

### Building on Linux

On Linux, after running `build.sh`, you can:

- Distribute the `dist/weatherapp` executable
- Create a `.deb` or `.rpm` package using `fpm` or similar tools
- Create an AppImage using `appimagetool`

## Development

### Project Structure

```
weatherapp/
├── src/
│   └── weatherapp/
│       ├── __init__.py
│       ├── __main__.py      # Entry point
│       ├── client.py        # Weather API client
│       ├── config.py        # Configuration management
│       ├── exceptions.py    # Custom exceptions
│       ├── gui.py           # Tkinter GUI
│       └── models.py        # Data models
├── .env.example             # Example environment file
├── build.sh                 # Build script for creating executable
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

### Running from Source

If you want to run the application without installing it:

```bash
python -m src.weatherapp
```

## Configuration

The application can be configured using environment variables in the `.env` file:

- `WEATHER_API_KEY`: Your WeatherAPI.com API key (required)

The default city is set to London. You can change this in `src/weatherapp/config.py`.

## API Information

This application uses the [WeatherAPI.com](https://www.weatherapi.com/) service. The free tier includes:
- Current weather data
- 3-day forecast (we use 5 days, which requires checking your plan)
- 1,000,000 calls per month

## Troubleshooting

### "API key is required" error

Make sure you have:
1. Created a `.env` file in the project root directory (or in the same directory as the executable)
2. Added your API key to the `.env` file:
   ```
   WEATHER_API_KEY=your_actual_api_key_here
   ```

### "Network error" or "Connection timeout"

- Check your internet connection
- Verify that the WeatherAPI.com service is accessible
- Some corporate firewalls may block the API requests

### City not found

- Double-check the spelling of the city name
- Try using a more specific name (e.g., "London, UK" instead of just "London")
- Some smaller cities may not be available in the database

### macOS Security Warning

If you see "WeatherApp.app can't be opened because it is from an unidentified developer":
1. Right-click (or Control-click) on WeatherApp.app
2. Select "Open" from the context menu
3. Click "Open" in the dialog that appears

Alternatively, you can run:
```bash
xattr -cr WeatherApp.app
```

## License

This project is provided as-is for educational purposes.

## Credits

Weather data provided by [WeatherAPI.com](https://www.weatherapi.com/)
