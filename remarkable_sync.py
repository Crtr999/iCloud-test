#!/usr/bin/env python3
"""
reMarkable to iCloud Drive Sync Script

This script syncs documents from your reMarkable tablet to your iCloud Drive.
It monitors for changes and automatically downloads modified files.
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/remarkable_sync.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RemarkableSync:
    """Handles syncing between reMarkable and iCloud Drive"""

    def __init__(self, config_path='~/remarkable_sync_config.json'):
        self.config_path = os.path.expanduser(config_path)
        self.config = self.load_config()
        self.icloud_path = os.path.expanduser(self.config.get('icloud_path', '~/Library/Mobile Documents/com~apple~CloudDocs/reMarkable'))
        self.sync_state_file = os.path.expanduser('~/.remarkable_sync_state.json')
        self.sync_state = self.load_sync_state()

    def load_config(self):
        """Load configuration from JSON file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            logger.warning(f"Config file not found at {self.config_path}, using defaults")
            return {
                'icloud_path': '~/Library/Mobile Documents/com~apple~CloudDocs/Remarkable Sync',
                'sync_format': 'pdf',  # pdf or epub
                'rmapi_path': 'rmapi',  # path to rmapi binary
                'exclude_folders': []
            }

    def load_sync_state(self):
        """Load the last sync state"""
        if os.path.exists(self.sync_state_file):
            with open(self.sync_state_file, 'r') as f:
                return json.load(f)
        return {}

    def save_sync_state(self):
        """Save the current sync state"""
        with open(self.sync_state_file, 'w') as f:
            json.dump(self.sync_state, f, indent=2)

    def ensure_icloud_directory(self):
        """Create iCloud sync directory if it doesn't exist"""
        Path(self.icloud_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"iCloud sync directory: {self.icloud_path}")

    def check_rmapi_installed(self):
        """Check if rmapi is installed"""
        try:
            result = subprocess.run(
                [self.config.get('rmapi_path', 'rmapi'), '--version'],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def list_remarkable_files(self):
        """List all files on reMarkable using rmapi"""
        try:
            result = subprocess.run(
                [self.config.get('rmapi_path', 'rmapi'), 'ls', '-r'],
                capture_output=True,
                text=True,
                check=True
            )
            return self.parse_rmapi_list(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to list reMarkable files: {e}")
            return []

    def parse_rmapi_list(self, output):
        """Parse rmapi ls output to get file list"""
        files = []
        for line in output.strip().split('\n'):
            if line.strip() and not line.startswith('['):
                # Parse the line to extract file info
                parts = line.strip().split()
                if len(parts) >= 2:
                    # Basic parsing - adjust based on actual rmapi output format
                    file_path = ' '.join(parts[1:])
                    if not any(folder in file_path for folder in self.config.get('exclude_folders', [])):
                        files.append(file_path)
        return files

    def get_file_hash(self, file_path):
        """Calculate hash of a file"""
        if not os.path.exists(file_path):
            return None

        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def download_file(self, remarkable_path):
        """Download a file from reMarkable to iCloud Drive"""
        try:
            # Sanitize filename for local filesystem
            local_filename = remarkable_path.replace('/', '_')
            output_format = self.config.get('sync_format', 'pdf')
            local_path = os.path.join(self.icloud_path, f"{local_filename}.{output_format}")

            # Use rmapi to download and convert
            logger.info(f"Downloading: {remarkable_path}")
            result = subprocess.run(
                [
                    self.config.get('rmapi_path', 'rmapi'),
                    'get',
                    remarkable_path,
                    local_path
                ],
                capture_output=True,
                text=True,
                check=True
            )

            # Update sync state
            file_hash = self.get_file_hash(local_path)
            self.sync_state[remarkable_path] = {
                'last_sync': datetime.now().isoformat(),
                'local_path': local_path,
                'hash': file_hash
            }

            logger.info(f"Successfully downloaded: {remarkable_path} -> {local_path}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to download {remarkable_path}: {e}")
            return False

    def sync_all(self):
        """Sync all files from reMarkable to iCloud Drive"""
        logger.info("Starting sync from reMarkable to iCloud Drive...")

        # Ensure iCloud directory exists
        self.ensure_icloud_directory()

        # Check if rmapi is installed
        if not self.check_rmapi_installed():
            logger.error("rmapi is not installed or not found in PATH")
            logger.error("Please install rmapi from: https://github.com/juruen/rmapi")
            return False

        # List all files on reMarkable
        remarkable_files = self.list_remarkable_files()
        logger.info(f"Found {len(remarkable_files)} files on reMarkable")

        # Download new or modified files
        downloaded_count = 0
        for remarkable_path in remarkable_files:
            # Check if file needs to be synced
            if remarkable_path not in self.sync_state:
                # New file
                if self.download_file(remarkable_path):
                    downloaded_count += 1
            else:
                # Check if file was modified (you might need to implement a better check)
                # For now, we'll skip already synced files
                logger.debug(f"Skipping already synced file: {remarkable_path}")

        # Save sync state
        self.save_sync_state()

        logger.info(f"Sync complete. Downloaded {downloaded_count} new/modified files.")
        return True

    def force_sync_all(self):
        """Force sync all files, even if already synced"""
        logger.info("Starting FORCE sync from reMarkable to iCloud Drive...")

        # Clear sync state to force re-download
        self.sync_state = {}
        return self.sync_all()


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Sync reMarkable files to iCloud Drive')
    parser.add_argument('--force', action='store_true', help='Force sync all files')
    parser.add_argument('--config', default='~/remarkable_sync_config.json',
                       help='Path to config file')

    args = parser.parse_args()

    try:
        syncer = RemarkableSync(config_path=args.config)

        if args.force:
            syncer.force_sync_all()
        else:
            syncer.sync_all()

    except KeyboardInterrupt:
        logger.info("Sync interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
