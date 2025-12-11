# Simple Installation Guide - reMarkable to iCloud Sync

## Super Simple 3-Step Setup

### Step 1: Uninstall Old Package & Install New One

Open Terminal and run:

```bash
pip3 uninstall rmapy
pip3 install rmcl
```

That's it. No binaries, no downloads, just one Python package (rmcl is the actively maintained version).

### Step 2: Run First-Time Setup

```bash
cd ~/iCloud-test
python3 remarkable_sync_v3.py --setup
```

This will:
1. Ask you to visit https://my.remarkable.com/device/desktop/connect
2. Show you a code on that page
3. You enter the code
4. Done! Your device is registered.

### Step 3: Sync Your Files

```bash
python3 remarkable_sync_v3.py
```

Your files will download to:
```
~/Library/Mobile Documents/com~apple~CloudDocs/Remarkable Sync/
```

## That's It!

Your files are now synced. Open Finder → iCloud Drive → Remarkable Sync to see them.

## Optional: Set Up Automatic Syncing

Want it to sync automatically every 15 minutes?

### Create Launch Agent

```bash
# Copy the plist file
cp com.remarkable.sync.v2.plist ~/Library/LaunchAgents/

# Edit paths in the file (replace /path/to/ with your actual path)
nano ~/Library/LaunchAgents/com.remarkable.sync.v2.plist

# Load it
launchctl load ~/Library/LaunchAgents/com.remarkable.sync.v2.plist

# Start it
launchctl start com.remarkable.sync.v2
```

Done! Now it syncs automatically every 15 minutes.

## Commands

**Sync now:**
```bash
python3 remarkable_sync_v3.py
```

**Force re-download everything:**
```bash
python3 remarkable_sync_v3.py --force
```

**Re-authenticate (if token expires):**
```bash
python3 remarkable_sync_v3.py --setup
```

**View logs:**
```bash
tail -f ~/remarkable_sync.log
```

## Troubleshooting

**"rmcl not installed" error:**
```bash
pip3 install rmcl
```

**Authentication fails:**
- Make sure you're entering the code quickly (it expires in ~30 seconds)
- Get a fresh code from https://my.remarkable.com/device/desktop/connect
- Try again

**No files syncing:**
- Check you have documents on your reMarkable
- Run with `--force` to re-download everything
- Check logs: `tail ~/remarkable_sync.log`

## Stop Automatic Sync

```bash
launchctl unload ~/Library/LaunchAgents/com.remarkable.sync.v2.plist
```

## Uninstall Everything

```bash
# Stop automatic sync
launchctl unload ~/Library/LaunchAgents/com.remarkable.sync.v2.plist

# Remove files
rm ~/Library/LaunchAgents/com.remarkable.sync.v2.plist
rm ~/.rmapi_token
rm ~/.remarkable_sync_state.json
rm ~/remarkable_sync.log
rm ~/remarkable_sync_config.json

# Optionally remove Python package
pip3 uninstall rmcl
```
