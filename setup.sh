#!/bin/bash
# Setup script for reMarkable to iCloud sync
# This installs everything you need automatically

set -e  # Exit on error

echo "=========================================="
echo "reMarkable to iCloud Sync - Setup"
echo "=========================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "ERROR: This script is for macOS only"
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew (this may take a few minutes)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✓ Homebrew is already installed"
fi

# Install rmapi (reMarkable API client)
if ! command -v rmapi &> /dev/null; then
    echo "Installing rmapi..."
    brew install rmapi
else
    echo "✓ rmapi is already installed"
fi

# Make sync script executable
chmod +x remarkable_sync.py

echo ""
echo "=========================================="
echo "First-time setup: Connecting to reMarkable"
echo "=========================================="
echo ""
echo "You need to authorize this computer to access your reMarkable."
echo "This is a ONE-TIME setup."
echo ""
echo "Running 'rmapi' for the first time..."
echo "Follow the instructions to get your one-time code."
echo ""

# Run rmapi to trigger authentication
rmapi ls || true

echo ""
echo "=========================================="
echo "Setting up automatic sync"
echo "=========================================="
echo ""

# Get current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create Launch Agent plist
PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="$PLIST_DIR/com.remarkable.sync.plist"

mkdir -p "$PLIST_DIR"

cat > "$PLIST_FILE" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.remarkable.sync</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$SCRIPT_DIR/remarkable_sync.py</string>
    </array>

    <key>StartInterval</key>
    <integer>3600</integer>

    <key>RunAtLoad</key>
    <true/>

    <key>StandardOutPath</key>
    <string>$HOME/.remarkable_sync_stdout.log</string>

    <key>StandardErrorPath</key>
    <string>$HOME/.remarkable_sync_stderr.log</string>
</dict>
</plist>
EOF

echo "✓ Created automatic sync configuration"

# Load the Launch Agent
launchctl unload "$PLIST_FILE" 2>/dev/null || true
launchctl load "$PLIST_FILE"

echo "✓ Automatic sync is now active"

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Your reMarkable will now automatically sync to iCloud every hour."
echo ""
echo "iCloud folder: ~/Library/Mobile Documents/com~apple~CloudDocs/Remarkable sync"
echo ""
echo "To access this folder in Finder:"
echo "  1. Open Finder"
echo "  2. Go to iCloud Drive (in sidebar)"
echo "  3. Look for 'Remarkable sync' folder"
echo ""
echo "Useful commands:"
echo "  - Run sync now:        ./remarkable_sync.py"
echo "  - View sync log:       tail -f ~/.remarkable_sync.log"
echo "  - Stop auto-sync:      launchctl unload ~/Library/LaunchAgents/com.remarkable.sync.plist"
echo "  - Start auto-sync:     launchctl load ~/Library/LaunchAgents/com.remarkable.sync.plist"
echo ""
echo "The first sync will start within the next minute!"
echo ""
