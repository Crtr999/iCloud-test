# reMarkable to iCloud Sync - Simple Setup Guide

## What This Does

Automatically syncs all your reMarkable documents to your iCloud Drive folder called "Remarkable sync" every hour. No manual work needed after setup!

---

## One-Time Setup (5 minutes)

### Step 1: Open Terminal

1. Press `Command + Space` to open Spotlight
2. Type `Terminal` and press Enter

### Step 2: Go to This Folder

Copy and paste this command into Terminal and press Enter:

```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Remarkable\ sync
```

If you get an error, the folder might be in a different location. Try:

```bash
cd ~/Desktop
```

Then drag the folder containing these files into the Terminal window.

### Step 3: Run the Setup

Copy and paste this command and press Enter:

```bash
bash setup.sh
```

### Step 4: Connect Your reMarkable

During setup, you'll see instructions to connect your reMarkable account:

1. Go to the website shown in Terminal
2. Get your one-time code
3. Type it into Terminal and press Enter

**That's it!** The sync will now run automatically every hour.

---

## How to Check It's Working

### Option 1: Look at Your iCloud Folder

1. Open Finder
2. Click "iCloud Drive" in the sidebar
3. Open the "Remarkable sync" folder
4. Your reMarkable documents should appear there

### Option 2: Check the Log

In Terminal, run:

```bash
tail -f ~/.remarkable_sync.log
```

Press `Control + C` to stop viewing the log.

---

## Troubleshooting

### "I don't see my files yet"

- The first sync happens within 1 minute of setup
- Then it runs every hour automatically
- To sync immediately, run: `./remarkable_sync.py`

### "I want to sync more often"

By default it syncs every hour. To change this:

1. Open Terminal
2. Run: `nano ~/Library/LaunchAgents/com.remarkable.sync.plist`
3. Find the line with `<integer>3600</integer>`
4. Change 3600 to:
   - 1800 = every 30 minutes
   - 900 = every 15 minutes
   - 300 = every 5 minutes
5. Press `Control + X`, then `Y`, then Enter to save
6. Run: `launchctl unload ~/Library/LaunchAgents/com.remarkable.sync.plist && launchctl load ~/Library/LaunchAgents/com.remarkable.sync.plist`

### "I want to stop automatic syncing"

```bash
launchctl unload ~/Library/LaunchAgents/com.remarkable.sync.plist
```

### "I want to start it again"

```bash
launchctl load ~/Library/LaunchAgents/com.remarkable.sync.plist
```

---

## How It Works

1. Every hour (or your chosen interval), the script connects to your reMarkable Cloud
2. Downloads all your documents and notebooks
3. Copies them to your "Remarkable sync" folder in iCloud Drive
4. iCloud automatically syncs to all your Apple devices

**You don't need to do anything!** Just use your reMarkable as normal, and your documents will appear in iCloud.

---

## Need Help?

Check the log file to see what's happening:

```bash
cat ~/.remarkable_sync.log
```

If you see errors, make sure:
- You're connected to the internet
- You completed the reMarkable authentication step
- Your iCloud Drive is working (check System Settings > Apple ID > iCloud)
