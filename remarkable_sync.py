#!/usr/bin/env python3
"""
reMarkable to iCloud Drive Sync
Automatically syncs all documents from reMarkable to iCloud Drive
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Configuration
ICLOUD_FOLDER = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Remarkable sync")
TEMP_DOWNLOAD_DIR = os.path.expanduser("~/.remarkable_temp")
LOG_FILE = os.path.expanduser("~/.remarkable_sync.log")

def log(message):
    """Log messages with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)

    with open(LOG_FILE, 'a') as f:
        f.write(log_message + "\n")

def ensure_directories():
    """Create necessary directories if they don't exist"""
    Path(ICLOUD_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(TEMP_DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)
    log(f"Ensured directories exist: {ICLOUD_FOLDER}")

def check_rmapi():
    """Check if rmapi is installed"""
    try:
        result = subprocess.run(['rmapi', 'version'],
                              capture_output=True,
                              text=True,
                              timeout=10)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def sync_remarkable_to_icloud():
    """Main sync function"""
    log("=" * 60)
    log("Starting reMarkable to iCloud sync")

    # Check if rmapi is installed
    if not check_rmapi():
        log("ERROR: rmapi is not installed or not in PATH")
        log("Please run the setup script first: ./setup.sh")
        return False

    ensure_directories()

    try:
        # Change to temp directory for downloads
        os.chdir(TEMP_DOWNLOAD_DIR)

        # List all documents on reMarkable
        log("Fetching document list from reMarkable...")
        result = subprocess.run(['rmapi', 'ls', '/'],
                              capture_output=True,
                              text=True,
                              timeout=30)

        if result.returncode != 0:
            log(f"ERROR: Failed to list reMarkable documents: {result.stderr}")
            return False

        # Get all items (files and folders)
        log("Downloading all documents from reMarkable...")
        download_result = subprocess.run(['rmapi', 'mget', '/'],
                                        capture_output=True,
                                        text=True,
                                        timeout=300)

        if download_result.returncode != 0:
            log(f"WARNING: Some files may not have downloaded: {download_result.stderr}")

        # Sync downloaded files to iCloud
        log("Copying files to iCloud Drive...")
        sync_count = 0

        for root, dirs, files in os.walk(TEMP_DOWNLOAD_DIR):
            for file in files:
                if file == '.DS_Store':
                    continue

                source_path = os.path.join(root, file)

                # Maintain folder structure
                rel_path = os.path.relpath(source_path, TEMP_DOWNLOAD_DIR)
                dest_path = os.path.join(ICLOUD_FOLDER, rel_path)

                # Create destination directory if needed
                Path(dest_path).parent.mkdir(parents=True, exist_ok=True)

                # Copy file if it's new or modified
                should_copy = False
                if not os.path.exists(dest_path):
                    should_copy = True
                else:
                    # Check if source is newer
                    source_mtime = os.path.getmtime(source_path)
                    dest_mtime = os.path.getmtime(dest_path)
                    if source_mtime > dest_mtime:
                        should_copy = True

                if should_copy:
                    subprocess.run(['cp', source_path, dest_path], check=True)
                    sync_count += 1
                    log(f"Synced: {rel_path}")

        log(f"Sync completed successfully! {sync_count} files updated")

        # Clean up temp directory
        subprocess.run(['rm', '-rf', TEMP_DOWNLOAD_DIR], check=True)
        Path(TEMP_DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

        return True

    except subprocess.TimeoutExpired:
        log("ERROR: Sync timed out. Check your internet connection.")
        return False
    except Exception as e:
        log(f"ERROR: Sync failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = sync_remarkable_to_icloud()
    sys.exit(0 if success else 1)
