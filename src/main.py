#!/usr/bin/env python3
"""
cmd-aegnt - A command-line AI agent for system tasks
"""

import sys
import os
import subprocess
import argparse
import json
import re

# Dictionary mapping natural language commands to system actions
COMMAND_MAPPINGS = {
    "screensaver": {
        "turn on": "gsettings set org.gnome.desktop.screensaver idle-activation-enabled true",
        "turn off": "gsettings set org.gnome.desktop.screensaver idle-activation-enabled false",
        "enable": "gsettings set org.gnome.desktop.screensaver idle-activation-enabled true",
        "disable": "gsettings set org.gnome.desktop.screensaver idle-activation-enabled false",
        "set timeout": lambda mins: f"gsettings set org.gnome.desktop.screensaver lock-delay {int(mins) * 60}"
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
    parser = argparse.ArgumentParser(description="AI agent for system tasks")
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
            
        print(f"Executing: {cmd}")
        success = execute_system_command(cmd)
        
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
