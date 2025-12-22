#!/bin/bash
# Siena's Snowy Adventure - Installer
# This removes the macOS quarantine flag so the game can run

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=========================================="
echo "Siena's Snowy Adventure - Mac Installer"
echo "=========================================="
echo ""
echo "Removing macOS security quarantine..."
echo ""

# Remove quarantine attribute
xattr -cr "$DIR/SienaSnowyAdventure.app"

if [ $? -eq 0 ]; then
    echo "✅ Success! The game is ready to play."
    echo ""
    echo "You can now close this window and"
    echo "double-click SienaSnowyAdventure.app to play!"
else
    echo "❌ Failed to remove quarantine."
    echo ""
    echo "You may need to manually run:"
    echo "xattr -cr ~/Downloads/SienaSnowyAdventure.app"
fi

echo ""
echo "Press Enter to close this window..."
read
