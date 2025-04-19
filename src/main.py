#!/usr/bin/env python3
"""
cmd-aegnt - A command-line AI aegnt for system tasks
"""

import sys
import os
import subprocess
import argparse
import json
import re
import time

# Dictionary mapping natural language commands to system actions
COMMAND_MAPPINGS = {
    "screensaver": {
        "turn on": "gsettings set org.gnome.desktop.screensaver idle-activation-enabled true",
        "turn off": "gsettings set org.gnome.desktop.screensaver idle-activation-enabled false",
        "enable": "gsettings set org.gnome.desktop.screensaver idle-activation-enabled true",
        "disable": "gsettings set org.gnome.desktop.screensaver idle-activation-enabled false",
        "set timeout": lambda mins: [
            f"gsettings set org.gnome.desktop.screensaver lock-delay {int(mins) * 60}"
        ],
        "set style": lambda style: f"gsettings set org.gnome.desktop.screensaver picture-uri '{style}'",
        "enable message": "gsettings set org.gnome.desktop.screensaver status-message-enabled true",
        "disable message": "gsettings set org.gnome.desktop.screensaver status-message-enabled false"
    },
    "volume": {
        "increase": "amixer -D pulse sset Master 5%+",
        "decrease": "amixer -D pulse sset Master 5%-",
        "mute": "amixer -D pulse sset Master mute",
        "unmute": "amixer -D pulse sset Master unmute",
        "set": lambda level: f"amixer -D pulse sset Master {level}%"
    },
    "brightness": {
        "increase": "xbacklight -inc 10",
        "decrease": "xbacklight -dec 10",
        "set": lambda level: f"xbacklight -set {level}"
    },
    "wifi": {
        "turn on": "nmcli radio wifi on",
        "turn off": "nmcli radio wifi off",
        "enable": "nmcli radio wifi on",
        "disable": "nmcli radio wifi off",
        "connect": lambda ssid: f"nmcli device wifi connect '{ssid}'"
    }
}

# Screensaver styles
SCREENSAVER_STYLES = {
    'a': {
        'name': 'Default Ubuntu Screensaver',
        'uri': 'file:///usr/share/backgrounds/ubuntu-wallpaper-d.png'
    },
    'b': {
        'name': 'Numbat Wallpaper',
        'uri': 'file:///usr/share/backgrounds/Numbat_wallpaper_dimmed_3480x2160.png'
    },
    'c': {
        'name': 'Fuji San',
        'uri': 'file:///usr/share/backgrounds/Fuji_san_by_amaral.png'
    },
    'd': {
        'name': 'Custom Message',
        'uri': 'file:///usr/share/backgrounds/ubuntu-wallpaper-d.png',
        'custom_message': True
    }
}

# User-friendly action names for output messages
ACTION_MESSAGES = {
    "turn on": "turned on",
    "turn off": "turned off",
    "enable": "enabled",
    "disable": "disabled",
    "set timeout": "set timeout for",
    "increase": "increased",
    "decrease": "decreased",
    "mute": "muted",
    "unmute": "unmuted",
    "set": "set",
    "connect": "connected to"
}

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="AI aegnt for system tasks")
    parser.add_argument("command", nargs="+", help="The natural language command to execute")
    return parser.parse_args()

def extract_command_intent(text):
    """Extract the intent from the command text."""
    text = text.lower()
    
    # Check for screensaver commands
    if any(word in text for word in ["screensaver", "screen saver"]):
        if any(phrase in text for phrase in ["on", "enable", "activate", "turn on", "back on"]):
            return ("screensaver", "turn on", None)
        elif any(phrase in text for phrase in ["off", "disable", "deactivate", "turn off"]):
            return ("screensaver", "turn off", None)
        elif "timeout" in text or "time" in text:
            # Extract number of minutes
            match = re.search(r'(\d+)\s*(?:minute|min)', text)
            if match:
                mins = match.group(1)
                return ("screensaver", "set timeout", mins)
    
    # Check for volume commands
    if "volume" in text:
        if any(word in text for word in ["up", "increase", "higher", "louder"]):
            return ("volume", "increase", None)
        elif any(word in text for word in ["down", "decrease", "lower", "quieter"]):
            return ("volume", "decrease", None)
        elif any(word in text for word in ["mute", "silent", "quiet"]):
            return ("volume", "mute", None)
        elif "unmute" in text:
            return ("volume", "unmute", None)
        elif "set" in text or "%" in text:
            match = re.search(r'(\d+)(?:\s*%)?', text)
            if match:
                level = match.group(1)
                return ("volume", "set", level)
    
    # Check for brightness commands
    if "brightness" in text:
        if any(word in text for word in ["up", "increase", "higher", "brighter"]):
            return ("brightness", "increase", None)
        elif any(word in text for word in ["down", "decrease", "lower", "dimmer"]):
            return ("brightness", "decrease", None)
        elif "set" in text or "%" in text:
            match = re.search(r'(\d+)(?:\s*%)?', text)
            if match:
                level = match.group(1)
                return ("brightness", "set", level)
    
    # Check for wifi commands
    if any(word in text for word in ["wifi", "wi-fi", "wireless"]):
        if any(phrase in text for phrase in ["on", "enable", "activate", "turn on"]):
            return ("wifi", "turn on", None)
        elif any(phrase in text for phrase in ["off", "disable", "deactivate", "turn off"]):
            return ("wifi", "turn off", None)
        elif "connect" in text:
            match = re.search(r'connect(?:\s+to)?\s+["\']?([^"\']+)["\']?', text, re.IGNORECASE)
            if match:
                ssid = match.group(1)
                return ("wifi", "connect", ssid)
    
    return None

def execute_system_command(command):
    """Execute a system command."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Command failed: {result.stderr}")
            return False
        
        if result.stdout:
            print(result.stdout)
        
        return True
    except Exception as e:
        print(f"Error executing command: {str(e)}")
        return False

def set_screensaver_timeout_via_dsktp_cmd_aegnt(minutes):
    """Set screensaver timeout using dsktp-cmd-aegnt."""
    try:
        cmd = f"dsktp-cmd-aegnt --text \"set screensaver timeout to {minutes} minutes\""
        print(f"Using dsktp-cmd-aegnt to set screensaver timeout: {cmd}")
        
        # Start the process
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Give it some time to work
        time.sleep(5)
        
        # Terminate the process (dsktp-cmd-aegnt doesn't exit automatically)
        process.terminate()
        
        return True
    except Exception as e:
        print(f"Error executing dsktp-cmd-aegnt: {str(e)}")
        return False

def handle_interactive_screensaver():
    """Handle interactive screensaver settings."""
    print("Sure, I'll help you turn on the screensaver. Do you prefer:")
    
    # Display options
    for key, style in SCREENSAVER_STYLES.items():
        print(f"Option {key}) [{style['name']}]")
    
    # Get user choice
    choice = input("Enter your choice (a/b/c/d): ").lower()
    
    # Validate choice
    while choice not in SCREENSAVER_STYLES:
        choice = input("Invalid choice. Please enter a, b, c, or d: ").lower()
    
    selected_style = SCREENSAVER_STYLES[choice]
    print(f"You selected: {selected_style['name']}")
    
    # Get custom message if needed
    custom_message = None
    if 'custom_message' in selected_style and selected_style['custom_message']:
        custom_message = input("Please enter your custom message: ")
        print(f"Custom message set to: {custom_message}")
    
    # Get timeout
    timeout_mins = input("Enter timeout in minutes before starting screensaver: ")
    while not timeout_mins.isdigit() or int(timeout_mins) < 1:
        timeout_mins = input("Please enter a valid number of minutes (must be at least 1): ")
    
    timeout_mins = int(timeout_mins)
    print(f"Screensaver will start after {timeout_mins} minutes of inactivity")
    
    # Apply settings
    commands = [
        # Enable screensaver
        "gsettings set org.gnome.desktop.screensaver idle-activation-enabled true",
        # Set lock delay (if lock is enabled)
        f"gsettings set org.gnome.desktop.screensaver lock-delay 0",
        # Set style/background
        f"gsettings set org.gnome.desktop.screensaver picture-uri '{selected_style['uri']}'"
    ]
    
    # Handle custom message if applicable
    if custom_message:
        commands.append("gsettings set org.gnome.desktop.screensaver status-message-enabled true")
        # Note: GNOME doesn't provide a direct way to set the custom message content
        # This is usually done via the GUI. We just enable the status message option.
        print("Note: Custom message is enabled, but you'll need to set the message content via the GNOME screensaver settings.")
    
    # Execute commands
    success = True
    for cmd in commands:
        print(f"Executing: {cmd}")
        if not execute_system_command(cmd):
            success = False
            break
    
    # Set timeout using dsktp-cmd-aegnt
    print(f"Setting screensaver timeout to {timeout_mins} minutes using dsktp-cmd-aegnt")
    if not set_screensaver_timeout_via_dsktp_cmd_aegnt(timeout_mins):
        print("Warning: Failed to set timeout via dsktp-cmd-aegnt. The screensaver will still work, but might not use your timeout setting.")
        # Try the direct method as a fallback
        print(f"Attempting fallback method for timeout...")
        execute_system_command(f"gsettings set org.gnome.desktop.session idle-delay {timeout_mins * 60}")
    
    if success:
        print(f"Successfully configured screensaver with {selected_style['name']} and {timeout_mins} minute timeout.")
    else:
        print("Failed to configure screensaver completely.")
    
    return success

def execute_multiple_commands(commands):
    """Execute multiple system commands."""
    if isinstance(commands, list):
        success = True
        for cmd in commands:
            print(f"Executing: {cmd}")
            if not execute_system_command(cmd):
                success = False
                break
        return success
    else:
        # Single command
        print(f"Executing: {commands}")
        return execute_system_command(commands)

def main():
    """Main entry point."""
    args = parse_args()
    
    # Combine all arguments into a single command
    command_text = " ".join(args.command)
    
    print(f"Processing command: {command_text}")
    
    # Extract intent from command
    intent = extract_command_intent(command_text)
    
    if not intent:
        print("I'm sorry, I don't understand that command.")
        return
    
    category, action, param = intent
    print(f"Recognized intent: {category} - {action}" + (f" - {param}" if param else ""))
    
    # Special case for screensaver timeout
    if category == "screensaver" and action == "set timeout" and param:
        mins = int(param)
        print(f"Setting screensaver timeout to {mins} minutes via dsktp-cmd-aegnt")
        success = set_screensaver_timeout_via_dsktp_cmd_aegnt(mins)
        
        # Also set the lock-delay as a fallback
        print(f"Setting lock-delay to {mins * 60} seconds")
        execute_system_command(f"gsettings set org.gnome.desktop.screensaver lock-delay {mins * 60}")
        
        if success:
            print(f"Successfully set timeout for screensaver to {mins} minutes")
        else:
            print(f"Warning: Failed to set screensaver timeout to {mins} minutes")
        return
    
    # Special case for interactive screensaver setup
    if category == "screensaver" and action == "turn on":
        return handle_interactive_screensaver()
    
    # Get the system command to execute
    if category in COMMAND_MAPPINGS and action in COMMAND_MAPPINGS[category]:
        cmd_template = COMMAND_MAPPINGS[category][action]
        
        if callable(cmd_template):
            if param is None:
                print(f"Error: Parameter required for {category} {action}")
                return
            cmd = cmd_template(param)
        else:
            cmd = cmd_template
        
        # Execute the command(s)
        success = execute_multiple_commands(cmd)
        
        # Get user-friendly action message
        action_msg = ACTION_MESSAGES.get(action, action)
        
        if success:
            print(f"Successfully {action_msg} {category}" + (f" to {param}" if param else ""))
        else:
            print(f"Failed to {action} {category}")
    else:
        print(f"I understand you want to {action} the {category}, but I don't know how to do that yet.")

if __name__ == "__main__":
    main()
