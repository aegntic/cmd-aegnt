# cmd-aegnt

A command-line AI agent that uses natural language to perform system tasks.

## Features
- Natural language command interpretation
- System settings manipulation (e.g., "turn on screensaver")
- Support for various system commands:
  - Screensaver control
  - Volume control
  - Brightness control
  - WiFi management

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/cmd-aegnt.git
cd cmd-aegnt

# Install dependencies
pip install -r requirements.txt

# Make the command executable and accessible
chmod +x ae
sudo ln -s $(pwd)/ae /usr/local/bin/ae
```

## Usage
```bash
ae turn the screensaver back on
ae increase the volume by 10%
ae set brightness to 50%
ae turn off wifi
```

## Supported Commands

### Screensaver
- `ae turn on screensaver`
- `ae turn off screensaver`
- `ae set screensaver timeout to 5 minutes`

### Volume
- `ae increase volume`
- `ae decrease volume`
- `ae mute volume`
- `ae unmute volume`
- `ae set volume to 70%`

### Brightness
- `ae increase brightness`
- `ae decrease brightness` 
- `ae set brightness to 80%`

### WiFi
- `ae turn on wifi`
- `ae turn off wifi`
- `ae connect to "My WiFi Network"`

## Requirements
- Python 3.6+
- Linux/Unix-based system with GNOME desktop environment (for some features)
