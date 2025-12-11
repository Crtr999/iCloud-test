#!/usr/bin/env python3
"""
reMarkable to iCloud Drive Sync Script (Pure Python - rmcl version)

This script syncs documents from your reMarkable tablet to your iCloud Drive.
Uses rmcl library (actively maintained) - NO external binaries required!
"""

import os
import sys
import json
import logging
import asyncio
from pathlib import Path
from datetime import datetime

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

try:
    from rmcl import Document, Folder, Item
    from rmcl.api import Client
    from rmcl.const import ROOT_ID
except ImportError:
    logger.error("rmcl library not installed!")
    logger.error("Install it with: pip3 install rmcl")
    sys.exit(1)


class RemarkableSync:
    """Handles syncing between reMarkable and iCloud Drive using rmcl"""

    def __init__(self, config_path='~/remarkable_sync_config.json'):
        self.config_path = os.path.expanduser(config_path)
        self.config = self.load_config()
        self.icloud_path = os.path.expanduser(self.config.get('icloud_path', '~/Library/Mobile Documents/com~apple~CloudDocs/Remarkable Sync'))
        self.sync_state_file = os.path.expanduser('~/.remarkable_sync_state.json')
        self.sync_state = self.load_sync_state()
        self.token_file = os.path.expanduser('~/.rmapi_token')
        self.client = None

    def load_config(self):
        """Load configuration from JSON file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            return {
                'icloud_path': '~/Library/Mobile Documents/com~apple~CloudDocs/Remarkable Sync',
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

    async def authenticate(self):
        """Authenticate with reMarkable cloud"""
        self.client = Client()

        # Check if we have a stored token
        if os.path.exists(self.token_file):
            try:
                logger.info("Using stored authentication token...")
                with open(self.token_file, 'r') as f:
                    token = f.read().strip()
                await self.client.register(token=token)
                logger.info("✓ Authentication successful (using stored token)")
                return True
            except Exception as e:
                logger.warning(f"Stored token invalid: {e}")
                logger.info("Will register new device...")

        # Need to register new device
        logger.info("")
        logger.info("=" * 60)
        logger.info("FIRST TIME SETUP - AUTHENTICATION REQUIRED")
        logger.info("=" * 60)
        logger.info("")
        logger.info("1. Go to: https://my.remarkable.com/device/desktop/connect")
        logger.info("2. You'll see a one-time code on that page")
        logger.info("3. Enter that code below (codes expire quickly!)")
        logger.info("")

        code = input("Enter one-time code: ").strip()

        try:
            await self.client.register(code)
            logger.info("✓ Device registered successfully!")

            # Save the token for future use
            token = self.client.token
            with open(self.token_file, 'w') as f:
                f.write(token)
            os.chmod(self.token_file, 0o600)  # Secure the token file
            logger.info(f"✓ Token saved to {self.token_file}")

            return True
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            logger.error("Make sure you entered the code quickly before it expired!")
            return False

    async def get_all_items(self):
        """Get all items from reMarkable"""
        try:
            items = await self.client.get_items()
            return items
        except Exception as e:
            logger.error(f"Error getting items: {e}")
            return []

    async def download_document(self, doc):
        """Download a document as PDF"""
        try:
            # Get document name
            name = doc.name or doc.id

            # Sanitize filename
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_', '.')).strip()
            if not safe_name:
                safe_name = doc.id

            local_path = os.path.join(self.icloud_path, f"{safe_name}.pdf")

            # Check if already synced
            if doc.id in self.sync_state:
                last_version = self.sync_state[doc.id].get('version', 0)
                current_version = doc.version
                if last_version == current_version:
                    logger.debug(f"Skipping unchanged: {safe_name}")
                    return False

            logger.info(f"Downloading: {safe_name}")

            # Download the document as PDF
            pdf_data = await self.client.download(doc.id, pdf=True)

            # Save as PDF
            with open(local_path, 'wb') as f:
                f.write(pdf_data)

            # Update sync state
            self.sync_state[doc.id] = {
                'name': safe_name,
                'last_sync': datetime.now().isoformat(),
                'local_path': local_path,
                'version': doc.version
            }

            logger.info(f"✓ Saved: {safe_name}.pdf")
            return True

        except Exception as e:
            logger.error(f"Failed to download {name}: {e}")
            return False

    async def sync_all(self):
        """Sync all files from reMarkable to iCloud Drive"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("Starting reMarkable to iCloud Drive Sync")
        logger.info("=" * 60)
        logger.info("")

        # Ensure iCloud directory exists
        self.ensure_icloud_directory()

        # Authenticate
        if not await self.authenticate():
            logger.error("Authentication failed. Cannot sync.")
            return False

        # Get all items
        logger.info("Fetching documents from reMarkable cloud...")
        items = await self.get_all_items()

        # Filter for documents only (not folders)
        documents = [item for item in items if isinstance(item, Document)]
        logger.info(f"Found {len(documents)} documents")

        if not documents:
            logger.info("No documents found on your reMarkable")
            return True

        # Download each document
        downloaded_count = 0
        for doc in documents:
            # Skip excluded folders
            if any(excluded in doc.name for excluded in self.config.get('exclude_folders', [])):
                continue

            if await self.download_document(doc):
                downloaded_count += 1

        # Save sync state
        self.save_sync_state()

        logger.info("")
        logger.info("=" * 60)
        logger.info(f"Sync complete! Downloaded {downloaded_count} new/updated files")
        logger.info(f"Files saved to: {self.icloud_path}")
        logger.info("=" * 60)
        logger.info("")

        return True

    async def force_sync_all(self):
        """Force sync all files, even if already synced"""
        logger.info("Starting FORCE sync (will re-download all files)...")
        # Clear sync state to force re-download
        self.sync_state = {}
        return await self.sync_all()


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync reMarkable files to iCloud Drive (Pure Python - No binaries required!)'
    )
    parser.add_argument('--force', action='store_true',
                       help='Force sync all files (re-download everything)')
    parser.add_argument('--config', default='~/remarkable_sync_config.json',
                       help='Path to config file')
    parser.add_argument('--setup', action='store_true',
                       help='Run first-time setup and authentication')

    args = parser.parse_args()

    syncer = RemarkableSync(config_path=args.config)

    try:
        if args.setup:
            logger.info("Running first-time setup...")
            asyncio.run(syncer.authenticate())
            logger.info("\nSetup complete! Run without --setup to sync your files.")
        elif args.force:
            asyncio.run(syncer.force_sync_all())
        else:
            asyncio.run(syncer.sync_all())

    except KeyboardInterrupt:
        logger.info("\nSync interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
