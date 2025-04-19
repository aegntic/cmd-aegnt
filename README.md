# cmd-aegnt

A command-line AI aegnt that uses natural language to perform system tasks.

## What is this?

This is a simple tool that lets you control your computer settings using plain English commands. For example, instead of navigating through system menus to change your screensaver, you can simply type:

```
ae turn the screensaver back on
```

And the tool will guide you through the process with easy-to-follow prompts.

## One-Step Installation

Copy and paste this single command into your terminal to install everything automatically:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/aegntic/cmd-aegnt/main/install.sh)"
```

This will:
- Download all necessary files
- Install any dependencies
- Set up the `ae` command for you
- Create the required `dsktp-cmd-aegnt` link
- Verify everything is working

After installation, you can immediately start using the `ae` command from anywhere.

## Usage Examples

```bash
# Control your screensaver
ae turn the screensaver back on
ae turn off screensaver
ae set screensaver timeout to 10 minutes

# Adjust volume
ae increase the volume
ae decrease volume
ae set volume to 70%
ae mute volume

# Control screen brightness
ae increase brightness
ae decrease brightness 
ae set brightness to 80%

# Manage WiFi
ae turn on wifi
ae turn off wifi
ae connect to "My WiFi Network"
```

## Screensaver Options

When you run `ae turn on screensaver`, you'll see options like:

```
Sure, I'll help you turn on the screensaver. Do you prefer:
Option a) [Default Ubuntu Screensaver]
Option b) [Numbat Wallpaper]
Option c) [Fuji San]
Option d) [Custom Message]
```

Select an option, set your timeout, and you're done!

## Manual Installation (if one-step method doesn't work)

If the automatic installation doesn't work for some reason, you can install manually:

```bash
# 1. Download the code
git clone https://github.com/aegntic/cmd-aegnt.git

# 2. Run the install script
cd cmd-aegnt
chmod +x install.sh
./install.sh
```
