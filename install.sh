#!/bin/bash

# Bold and colored text
BOLD=$(tput bold)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
RESET=$(tput sgr0)

echo "${BOLD}${GREEN}📱 Setting up cmd-aegnt...${RESET}"
echo ""

# Check if we're running the script from the repository or downloading it
if [ ! -d ".git" ] && [ ! -f "src/main.py" ]; then
  echo "${BOLD}${BLUE}Downloading cmd-aegnt...${RESET}"
  
  # Check if git is installed
  if ! command -v git &> /dev/null; then
    echo "${BOLD}${YELLOW}Git not found. Installing git...${RESET}"
    sudo apt-get update
    sudo apt-get install -y git
  fi
  
  git clone https://github.com/aegntic/cmd-aegnt.git
  cd cmd-aegnt
  echo ""
fi

# Make sure the ae script is executable
chmod +x ae

# Create personal bin directory if it doesn't exist
mkdir -p ~/bin

# Create symlink to the ae script
ln -sf "$(pwd)/ae" ~/bin/ae

# Add ~/bin to PATH if it's not already there
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
  echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
  echo 'export PATH="$HOME/bin:$PATH"' >> ~/.profile
  export PATH="$HOME/bin:$PATH"
fi

# Check if desktop-commander is installed
if ! command -v desktop-commander &> /dev/null; then
  echo "${BOLD}${YELLOW}desktop-commander not found. Installing...${RESET}"
  
  # Check if npm is installed
  if ! command -v npm &> /dev/null; then
    echo "${BOLD}${YELLOW}npm not found. Installing node.js and npm...${RESET}"
    sudo apt-get update
    sudo apt-get install -y nodejs npm
  fi
  
  # Install desktop-commander globally
  npm install -g desktop-commander
fi

# Create symlink from desktop-commander to dsktp-cmd-aegnt
sudo ln -sf "$(which desktop-commander)" /usr/local/bin/dsktp-cmd-aegnt

echo ""
echo "${BOLD}${GREEN}✅ Installation complete!${RESET}"
echo ""
echo "${BOLD}You can now use the 'ae' command. Try:${RESET}"
echo "  ae turn the screensaver back on"
echo "  ae increase volume"
echo "  ae set brightness to 70%"
echo ""
echo "${BOLD}If 'ae' command doesn't work immediately, try:${RESET}"
echo "  source ~/.bashrc"
echo "  or start a new terminal window"
