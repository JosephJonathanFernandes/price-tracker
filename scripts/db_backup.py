"""
Script to backup the SQLite database.
"""
import shutil
import os
from datetime import datetime

DB_NAME = "price_tracker.db"
BACKUP_DIR = "backups"

os.makedirs(BACKUP_DIR, exist_ok=True)
backup_file = os.path.join(BACKUP_DIR, f"{DB_NAME}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak")
shutil.copy2(DB_NAME, backup_file)
print(f"Database backed up to {backup_file}")
