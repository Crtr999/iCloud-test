# reMarkable to iCloud Drive Sync Setup

This guide will help you set up automatic syncing between your reMarkable tablet and iCloud Drive.

## Prerequisites

1. **macOS** (required for iCloud Drive integration)
2. **Python 3.6+** installed
3. **reMarkable tablet** with an active account
4. **iCloud Drive** enabled on your Mac

## Step 1: Install rmapi

`rmapi` is a command-line tool to access your reMarkable cloud.

### Installation Options:

**Option A: Using Homebrew (Recommended)**
```bash
brew install rmapi
```

**Option B: Using Go**
```bash
go install github.com/juruen/rmapi@latest
```

**Option C: Download Binary**
Download from: https://github.com/juruen/rmapi/releases

### Authenticate rmapi

After installation, authenticate with your reMarkable account:

```bash
rmapi
```

On first run, it will prompt you to:
1. Visit a URL
2. Enter a one-time code displayed in your terminal
3. Your device will be registered

Test the connection:
```bash
rmapi ls
```

You should see your reMarkable documents listed.

## Step 2: Configure the Sync Script

1. **Copy configuration file to your home directory:**

```bash
cp remarkable_sync_config.json ~/remarkable_sync_config.json
```

2. **Edit the configuration** (`~/remarkable_sync_config.json`):

```json
{
  "icloud_path": "~/Library/Mobile Documents/com~apple~CloudDocs/reMarkable",
  "sync_format": "pdf",
  "rmapi_path": "rmapi",
  "exclude_folders": [],
  "sync_interval_minutes": 15
}
```

**Configuration Options:**

- `icloud_path`: Where to sync files in iCloud Drive (folder will be created automatically)
- `sync_format`: Export format (`pdf` or `epub`)
- `rmapi_path`: Path to rmapi binary (use `which rmapi` to find it)
- `exclude_folders`: List of folder names to skip (e.g., `["Archive", "Trash"]`)
- `sync_interval_minutes`: How often to run automatic sync

3. **Make the sync script executable:**

```bash
chmod +x remarkable_sync.py
```

## Step 3: Test Manual Sync

Run a manual sync to test everything works:

```bash
python3 remarkable_sync.py
```

Or force sync all files:

```bash
python3 remarkable_sync.py --force
```

Check your iCloud Drive folder to verify files are syncing:
```bash
open ~/Library/Mobile\ Documents/com~apple~CloudDocs/reMarkable
```

## Step 4: Set Up Automatic Syncing

### Option A: Using launchd (macOS - Recommended)

1. **Create the launch agent:**

```bash
cp com.remarkable.sync.plist ~/Library/LaunchAgents/
```

2. **Edit the plist file** to update paths if needed:

```bash
nano ~/Library/LaunchAgents/com.remarkable.sync.plist
```

Make sure these paths are correct:
- Path to Python 3
- Path to `remarkable_sync.py`
- Path to config file

3. **Load the launch agent:**

```bash
launchctl load ~/Library/LaunchAgents/com.remarkable.sync.plist
```

4. **Start the service:**

```bash
launchctl start com.remarkable.sync
```

5. **Verify it's running:**

```bash
launchctl list | grep remarkable
```

### Option B: Using Cron (Alternative)

1. **Edit crontab:**

```bash
crontab -e
```

2. **Add this line** to run sync every 15 minutes:

```cron
*/15 * * * * /usr/bin/python3 /path/to/remarkable_sync.py >> ~/remarkable_sync.log 2>&1
```

Replace `/path/to/remarkable_sync.py` with the actual path to the script.

## Step 5: Monitor Sync

View sync logs:

```bash
tail -f ~/remarkable_sync.log
```

Check sync status:
```bash
cat ~/.remarkable_sync_state.json
```

## Troubleshooting

### rmapi not authenticated
```bash
rmapi
# Follow authentication steps
```

### Files not appearing in iCloud
1. Make sure iCloud Drive is enabled in System Preferences
2. Check available iCloud storage
3. Verify the sync path exists and is accessible
4. Check logs for errors: `cat ~/remarkable_sync.log`

### Sync script errors
```bash
# Run with verbose output
python3 remarkable_sync.py --force
```

### Disable automatic sync
```bash
# For launchd
launchctl unload ~/Library/LaunchAgents/com.remarkable.sync.plist

# For cron
crontab -e  # Remove the sync line
```

## Usage

### Manual Commands

**Sync new/modified files:**
```bash
python3 remarkable_sync.py
```

**Force sync all files:**
```bash
python3 remarkable_sync.py --force
```

**Use custom config:**
```bash
python3 remarkable_sync.py --config /path/to/config.json
```

### Automatic Sync

Once set up with launchd or cron, the sync will run automatically at your configured interval. Files you edit on your reMarkable will appear in your iCloud Drive folder within minutes.

## File Organization

Files are synced to: `~/Library/Mobile Documents/com~apple~CloudDocs/reMarkable/`

You can access these files:
- In Finder: Go > iCloud Drive > reMarkable folder
- On iPhone/iPad: Files app > iCloud Drive > reMarkable folder
- On iCloud.com: Files section

## Advanced Configuration

### Export Format

Change `sync_format` in config to switch between PDF and ePub:
- `"pdf"`: Best for annotated documents and handwritten notes
- `"epub"`: Best for e-books

### Exclude Folders

To skip certain folders:
```json
{
  "exclude_folders": ["Archive", "Trash", "Templates"]
}
```

### Custom Sync Interval

For launchd, edit the plist file's `StartInterval` value (in seconds):
- 900 = 15 minutes
- 1800 = 30 minutes
- 3600 = 1 hour

## Uninstall

1. Stop automatic sync:
```bash
launchctl unload ~/Library/LaunchAgents/com.remarkable.sync.plist
rm ~/Library/LaunchAgents/com.remarkable.sync.plist
```

2. Remove config and state files:
```bash
rm ~/remarkable_sync_config.json
rm ~/.remarkable_sync_state.json
rm ~/remarkable_sync.log
```

3. Optionally remove synced files:
```bash
rm -rf ~/Library/Mobile\ Documents/com~apple~CloudDocs/reMarkable
```

## Support

- rmapi documentation: https://github.com/juruen/rmapi
- reMarkable support: https://support.remarkable.com
- File issues: [Your repository URL]

## Notes

- The script only syncs FROM reMarkable TO iCloud (one-way sync)
- Files are exported as PDF/ePub, not in native reMarkable format
- Changes made to files in iCloud will NOT sync back to reMarkable
- Large notebooks may take time to export and sync
