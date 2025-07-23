#!/bin/bash

# Set backup directory
BACKUP_DIR="/home/raspberry/MakietaRefactor/backups"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Timestamp format
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Backup file name
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.db"

# Path to your actual database
DB_PATH="/home/raspberry/MakietaRefactor/API/database/items.db"

# Copy the database
cp "$DB_PATH" "$BACKUP_FILE"

echo "Backup created at: $BACKUP_FILE"

# --- Cleanup: Keep only the latest 10 backups ---
cd "$BACKUP_DIR" || exit
ls -1t db_backup_*.db | tail -n +11 | xargs -d '\n' rm -f --

echo "Old backups cleaned up. Only the 10 most recent are kept."

