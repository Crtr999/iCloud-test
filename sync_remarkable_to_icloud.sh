#!/bin/bash
#
# Dead Simple reMarkable to iCloud Sync
# No API, no authentication - just copies files
#

# Possible locations for reMarkable Mac app files
POSSIBLE_DIRS=(
    "$HOME/Library/Application Support/remarkable/desktop"
    "$HOME/.local/share/remarkable/desktop"
    "$HOME/Library/Containers/com.remarkable.desktop/Data/Library/Application Support/remarkable"
)

# iCloud destination
ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Remarkable Sync"

# Create iCloud folder if it doesn't exist
mkdir -p "$ICLOUD_DIR"

# Find the reMarkable directory
REMARKABLE_DIR=""
for DIR in "${POSSIBLE_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        REMARKABLE_DIR="$DIR"
        echo "📁 Found reMarkable files at: $DIR"
        break
    fi
done

# Check if we found it
if [ -z "$REMARKABLE_DIR" ]; then
    echo "❌ reMarkable Mac app folder not found!"
    echo ""
    echo "Searched in:"
    for DIR in "${POSSIBLE_DIRS[@]}"; do
        echo "  - $DIR"
    done
    echo ""
    echo "Please make sure the reMarkable Mac app is installed and has synced at least once."
    echo "Download from: https://remarkable.com"
    exit 1
fi

echo "🔄 Syncing reMarkable files to iCloud Drive..."

# Copy all PDF and EPUB files
find "$REMARKABLE_DIR" -type f \( -name "*.pdf" -o -name "*.epub" \) -exec cp {} "$ICLOUD_DIR/" \;

# Count files
FILE_COUNT=$(ls -1 "$ICLOUD_DIR" 2>/dev/null | wc -l)

echo "✅ Done! $FILE_COUNT files in iCloud Drive → Remarkable Sync"
echo "📂 Location: Finder → iCloud Drive → Remarkable Sync"
