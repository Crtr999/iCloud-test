# ACTUALLY SIMPLE Setup - No Bullshit

## What This Does

1. reMarkable desktop app syncs your tablet → your Mac
2. Simple script copies files → iCloud Drive
3. Runs automatically every 15 minutes

**Zero authentication. Zero APIs. Just works.**

---

## Step 1: Install reMarkable Desktop App

Download and install: **https://remarkable.com/desktop**

Launch it and sign in. It will start syncing your files to your Mac automatically.

---

## Step 2: Run This ONE Command

```bash
cd ~/iCloud-test
chmod +x sync_remarkable_to_icloud.sh
./sync_remarkable_to_icloud.sh
```

Your files are now in **iCloud Drive → Remarkable Sync**

---

## Step 3: Set Up Auto-Sync (Optional)

To make it run automatically every 15 minutes:

```bash
cp com.remarkable.autosync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.remarkable.autosync.plist
launchctl start com.remarkable.autosync
```

**Done.** Files will auto-sync every 15 minutes.

---

## That's It

- **Manual sync anytime:** `~/iCloud-test/sync_remarkable_to_icloud.sh`
- **View logs:** `tail ~/remarkable_autosync.log`
- **Stop auto-sync:** `launchctl stop com.remarkable.autosync`
- **Files location:** Finder → iCloud Drive → Remarkable Sync

No Python. No authentication. No pain.
