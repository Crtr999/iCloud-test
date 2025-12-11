#!/bin/bash
#
# reMarkable to iCloud Sync - Installation Script
#
# This script helps set up automatic syncing between reMarkable and iCloud Drive
#

set -e

echo "=========================================="
echo "reMarkable to iCloud Drive Sync - Setup"
echo "=========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "ERROR: This script requires macOS for iCloud Drive integration"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
USERNAME=$(whoami)
HOME_DIR="$HOME"

echo "Step 1: Checking prerequisites..."
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check for rmapi
if ! command -v rmapi &> /dev/null; then
    echo "WARNING: rmapi is not installed"
    echo ""
    echo "rmapi is required to access your reMarkable cloud."
    echo "Install options:"
    echo "  1. Homebrew: brew install rmapi"
    echo "  2. Go: go install github.com/juruen/rmapi@latest"
    echo "  3. Download: https://github.com/juruen/rmapi/releases"
    echo ""
    read -p "Would you like to install rmapi via Homebrew now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v brew &> /dev/null; then
            brew install rmapi
        else
            echo "ERROR: Homebrew is not installed"
            echo "Please install Homebrew from https://brew.sh/"
            exit 1
        fi
    else
        echo "Please install rmapi manually and run this script again"
        exit 1
    fi
fi
echo "✓ rmapi found: $(which rmapi)"

echo ""
echo "Step 2: Configuring sync..."
echo ""

# Copy config file
CONFIG_FILE="$HOME_DIR/remarkable_sync_config.json"
if [ -f "$CONFIG_FILE" ]; then
    echo "⚠ Config file already exists at $CONFIG_FILE"
    read -p "Overwrite? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp "$SCRIPT_DIR/remarkable_sync_config.json" "$CONFIG_FILE"
        echo "✓ Config file updated"
    else
        echo "✓ Keeping existing config file"
    fi
else
    cp "$SCRIPT_DIR/remarkable_sync_config.json" "$CONFIG_FILE"
    echo "✓ Config file created at $CONFIG_FILE"
fi

# Make sync script executable
chmod +x "$SCRIPT_DIR/remarkable_sync.py"
echo "✓ Sync script is executable"

echo ""
echo "Step 3: Testing rmapi authentication..."
echo ""

# Test rmapi
if rmapi ls &> /dev/null; then
    echo "✓ rmapi is authenticated and working"
else
    echo "⚠ rmapi is not authenticated"
    echo ""
    echo "Please authenticate rmapi now..."
    echo "You will be prompted to visit a URL and enter a code."
    echo ""
    read -p "Press Enter to continue..."
    rmapi
fi

echo ""
echo "Step 4: Testing sync..."
echo ""

# Run a test sync
echo "Running test sync..."
python3 "$SCRIPT_DIR/remarkable_sync.py" --config "$CONFIG_FILE"

echo ""
echo "Step 5: Setting up automatic sync..."
echo ""

# Setup launchd
PLIST_SRC="$SCRIPT_DIR/com.remarkable.sync.plist"
PLIST_DEST="$HOME_DIR/Library/LaunchAgents/com.remarkable.sync.plist"

# Create customized plist
cp "$PLIST_SRC" "$PLIST_DEST"

# Update paths in plist
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|/path/to/remarkable_sync.py|$SCRIPT_DIR/remarkable_sync.py|g" "$PLIST_DEST"
    sed -i '' "s|/Users/YOUR_USERNAME|$HOME_DIR|g" "$PLIST_DEST"
else
    sed -i "s|/path/to/remarkable_sync.py|$SCRIPT_DIR/remarkable_sync.py|g" "$PLIST_DEST"
    sed -i "s|/Users/YOUR_USERNAME|$HOME_DIR|g" "$PLIST_DEST"
fi

echo "✓ Launch agent created at $PLIST_DEST"

# Load launch agent
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"
echo "✓ Launch agent loaded"

# Start the service
launchctl start com.remarkable.sync
echo "✓ Sync service started"

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Your reMarkable files will now sync automatically every 15 minutes to:"
echo "  $HOME_DIR/Library/Mobile Documents/com~apple~CloudDocs/reMarkable"
echo ""
echo "Useful Commands:"
echo "  View logs:        tail -f ~/remarkable_sync.log"
echo "  Manual sync:      python3 $SCRIPT_DIR/remarkable_sync.py"
echo "  Force sync all:   python3 $SCRIPT_DIR/remarkable_sync.py --force"
echo "  Stop auto-sync:   launchctl stop com.remarkable.sync"
echo "  Start auto-sync:  launchctl start com.remarkable.sync"
echo "  Uninstall:        launchctl unload $PLIST_DEST"
echo ""
echo "Check your iCloud Drive to see your synced files!"
echo ""
