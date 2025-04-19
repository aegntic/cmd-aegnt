# cmd-aegnt

A command-line AI agent that uses natural language to perform system tasks.

## Features
- Natural language command interpretation
- System settings manipulation (e.g., "turn on screensaver")
- Interactive option selection for complex tasks
- Support for various system commands:
  - Screensaver control with style options
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
sudo ln -s /path/to/cmd-aegnt/ae /usr/local/bin/ae
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
- `ae turn on screensaver` (interactive mode with options)
- `ae turn off screensaver`
- `ae set screensaver timeout to 5 minutes`

#### Interactive Screensaver Options
When you run `ae turn on screensaver`, the tool will present you with options:
```
Sure, I'll help you turn on the screensaver. Do you prefer:
Option a) [Default Ubuntu Screensaver]
Option b) [Numbat Wallpaper]
Option c) [Fuji San]
Option d) [Custom Message]
```

If you select option d (Custom Message), it will prompt you to enter your custom message.
Then it will ask for the timeout in minutes before starting the screensaver.

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

## Project Summary

Here's a summary of what we've built:

1. A command-line tool called "ae" that interprets natural language commands
2. System task automation with support for:
   * Screensaver control with interactive style selection
   * Volume management
   * Brightness settings
   * WiFi control

The implementation:
* Uses Python's standard libraries
* Parses natural language into intents
* Maps intents to system commands
* Provides interactive option selection for complex tasks
* Executes the appropriate actions
* Provides user-friendly feedback

### How to Use

You can use the "ae" command like this:

```bash
cd cmd-aegnt
./ae turn the screensaver back on
./ae increase volume
./ae set brightness to 70%
./ae turn off wifi
```

For system-wide access, you can create a symbolic link:

```bash
sudo ln -s /path/to/cmd-aegnt/ae /usr/local/bin/ae
```

### Future Enhancements

1. Integration with AI services for more complex natural language understanding
2. Support for more system settings and applications
3. Support for multi-step commands
4. A configuration file for customizing commands
5. System-specific adaptations for different desktop environments
6. More interactive dialogs for other features

## Requirements
- Python 3.6+
- Linux/Unix-based system with GNOME desktop environment (for some features)
