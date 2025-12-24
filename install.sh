#!/bin/bash

# Siena's Snowy Adventure - Mac Installer
# This script downloads and installs the latest version of the game

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════╗"
echo "║   Siena's Snowy Adventure - Installer    ║"
echo "╔═══════════════════════════════════════════╗"
echo -e "${NC}"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}Error: This installer is for macOS only.${NC}"
    exit 1
fi

echo -e "${BLUE}[1/5]${NC} Preparing installation..."
sleep 1

# Create temporary directory
TEMP_DIR=$(mktemp -d)
ZIP_FILE="$TEMP_DIR/SienaSnowyAdventure.zip"
APP_NAME="SienaSnowyAdventure.app"

echo -e "${BLUE}[2/5]${NC} Downloading the latest version..."
echo -e "${YELLOW}This may take a minute depending on your internet speed...${NC}"

# Download the latest release (v1.2.7)
DOWNLOAD_URL="https://github.com/18drider360/siena_snowy_adventure/releases/download/v1.2.7/SienaSnowyAdventure-Mac-v1.2.7.zip"

if ! curl -L -# -o "$ZIP_FILE" "$DOWNLOAD_URL" 2>&1; then
    echo -e "${RED}Error: Failed to download the game.${NC}"
    echo "Please check your internet connection and try again."
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}✓ Download complete!${NC}"
echo ""

echo -e "${BLUE}[3/5]${NC} Extracting files..."
if ! unzip -q "$ZIP_FILE" -d "$TEMP_DIR" 2>&1; then
    echo -e "${RED}Error: Failed to extract files.${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}✓ Files extracted!${NC}"
echo ""

echo -e "${BLUE}[4/5]${NC} Installing to Applications folder..."

# Remove old version if it exists
if [ -d "/Applications/$APP_NAME" ]; then
    echo -e "${YELLOW}Removing previous version...${NC}"
    rm -rf "/Applications/$APP_NAME"
fi

# Move app to Applications
if ! mv "$TEMP_DIR/$APP_NAME" /Applications/ 2>&1; then
    echo -e "${RED}Error: Failed to move app to Applications folder.${NC}"
    echo "You may need to enter your password to allow this."
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}✓ Installed to Applications!${NC}"
echo ""

echo -e "${BLUE}[5/5]${NC} Removing macOS security restrictions..."
# Remove quarantine attribute to avoid Gatekeeper warnings
if xattr -d com.apple.quarantine "/Applications/$APP_NAME" 2>/dev/null; then
    echo -e "${GREEN}✓ Security settings configured!${NC}"
else
    echo -e "${YELLOW}Note: You may need to right-click the app and select 'Open' the first time.${NC}"
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Installation Complete! 🎉            ║${NC}"
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo ""
echo -e "The game has been installed to your Applications folder."
echo -e "You can now find it in ${BLUE}Applications > SienaSnowyAdventure${NC}"
echo ""
echo -e "${YELLOW}Would you like to launch the game now? (y/n)${NC}"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Launching game...${NC}"
    open "/Applications/$APP_NAME"
    echo ""
    echo -e "${GREEN}Enjoy playing Siena's Snowy Adventure! ⛷️${NC}"
else
    echo ""
    echo -e "${BLUE}To play later, find the game in your Applications folder!${NC}"
fi

echo ""
echo -e "${YELLOW}Tip: The game will automatically check for updates when you play!${NC}"
echo ""
