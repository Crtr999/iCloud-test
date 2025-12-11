# reMarkable to iCloud Drive Sync

Automatically sync your reMarkable tablet files to iCloud Drive for easy access across all your Apple devices.

## Features

- 🔄 Automatic syncing from reMarkable to iCloud Drive
- 📄 Export as PDF or ePub format
- ⏱️ Configurable sync intervals
- 📁 Folder exclusion support
- 📊 Sync state tracking to avoid redundant downloads
- 🚀 Easy installation with automated setup script

## Quick Start

### Prerequisites

- macOS (required for iCloud Drive)
- Python 3.6+
- reMarkable tablet with an active account
- iCloud Drive enabled

### Installation

1. **Clone this repository:**
   ```bash
   git clone <repository-url>
   cd iCloud-test
   ```

2. **Run the installation script:**
   ```bash
   chmod +x install_sync.sh
   ./install_sync.sh
   ```

   The script will:
   - Check prerequisites
   - Install rmapi (if needed)
   - Configure the sync settings
   - Authenticate with your reMarkable account
   - Set up automatic syncing
   - Run an initial test sync

3. **Done!** Your reMarkable files will now sync automatically every 15 minutes.

### Manual Setup

If you prefer to set things up manually, see [REMARKABLE_SYNC_SETUP.md](REMARKABLE_SYNC_SETUP.md) for detailed instructions.

## Usage

### Automatic Sync

Once installed, files sync automatically every 15 minutes to:
```
~/Library/Mobile Documents/com~apple~CloudDocs/Remarkable Sync/
```

Access your files from:
- **Finder:** Go → iCloud Drive → Remarkable Sync folder
- **iPhone/iPad:** Files app → iCloud Drive → Remarkable Sync folder
- **Web:** iCloud.com → Files section

### Manual Sync

Run a manual sync anytime:
```bash
python3 remarkable_sync.py
```

Force re-sync all files:
```bash
python3 remarkable_sync.py --force
```

### Configuration

Edit `~/remarkable_sync_config.json` to customize:

```json
{
  "icloud_path": "~/Library/Mobile Documents/com~apple~CloudDocs/Remarkable Sync",
  "sync_format": "pdf",
  "rmapi_path": "rmapi",
  "exclude_folders": [],
  "sync_interval_minutes": 15
}
```

## Monitoring

View sync logs:
```bash
tail -f ~/remarkable_sync.log
```

Check sync status:
```bash
cat ~/.remarkable_sync_state.json
```

## Troubleshooting

See [REMARKABLE_SYNC_SETUP.md](REMARKABLE_SYNC_SETUP.md#troubleshooting) for common issues and solutions.

## Files

- `remarkable_sync.py` - Main sync script
- `remarkable_sync_config.json` - Configuration template
- `com.remarkable.sync.plist` - macOS LaunchAgent configuration
- `install_sync.sh` - Automated installation script
- `REMARKABLE_SYNC_SETUP.md` - Detailed setup and usage guide

## How It Works

1. The script uses [rmapi](https://github.com/juruen/rmapi) to access your reMarkable cloud
2. It lists all documents on your reMarkable
3. New or modified files are downloaded and converted to PDF/ePub
4. Files are saved to your iCloud Drive folder
5. Sync state is tracked to avoid redundant downloads
6. The process runs automatically via macOS LaunchAgent

## Limitations

- **One-way sync only:** Changes sync FROM reMarkable TO iCloud (not bidirectional)
- **macOS only:** Requires iCloud Drive (macOS/iOS)
- **Export format:** Files are converted to PDF/ePub, not native reMarkable format
- **No live sync:** Files sync at configured intervals, not in real-time

## Dependencies

- [rmapi](https://github.com/juruen/rmapi) - Command-line tool for reMarkable cloud access
- Python 3.6+ (standard library only, no additional packages required)

## License

[Your License]

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Support

- For rmapi issues: https://github.com/juruen/rmapi
- For reMarkable support: https://support.remarkable.com
