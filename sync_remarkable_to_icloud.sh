#!/bin/bash
#
# Dead Simple reMarkable to iCloud Sync
# No API, no authentication - just copies files
#

# Where reMarkable desktop app stores files
REMARKABLE_DIR="$HOME/.local/share/remarkable/desktop"

# iCloud destination
ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Remarkable Sync"

# Create iCloud folder if it doesn't exist
mkdir -p "$ICLOUD_DIR"

# Check if reMarkable desktop folder exists
if [ ! -d "$REMARKABLE_DIR" ]; then
    echo "❌ reMarkable desktop app folder not found!"
    echo "Please install the reMarkable desktop app from:"
    echo "https://remarkable.com/desktop"
    exit 1
fi

echo "🔄 Syncing reMarkable files to iCloud Drive..."

# Copy all PDF and EPUB files
find "$REMARKABLE_DIR" -type f \( -name "*.pdf" -o -name "*.epub" \) -exec cp {} "$ICLOUD_DIR/" \;

# Count files
FILE_COUNT=$(ls -1 "$ICLOUD_DIR" 2>/dev/null | wc -l)

echo "✅ Done! $FILE_COUNT files in iCloud Drive → Remarkable Sync"
echo "📂 Location: Finder → iCloud Drive → Remarkable Sync"
