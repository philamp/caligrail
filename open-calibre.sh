#!/bin/bash

# you must test first 
# - your SSH access
# - Calibre URL 

# === Config ===
cd "$(dirname "$0")"
. open-calibre.env

# === Fonctions ===
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# === Vérification du montage ===
if mountpoint -q "$DEVICE_MOUNT"; then
    log "✅ eReader detected on $DEVICE_MOUNT"
else
    log "❌ No eReader detected on $DEVICE_MOUNT"
    exit 1
fi

# === Rsync ===
log "🚀 Starting rsync to Calibre $SSH_USER@$SSH_HOST:$TARGET_DIR ..."
rsync -avh --progress --delete -e ssh "$DEVICE_MOUNT"/ "$SSH_USER@$SSH_HOST:$TARGET_DIR"/
STATUS=$?

if [ $STATUS -eq 0 ]; then
    log "✅ Sync successful. Now Opening the web browser to open Calibre"
    xdg-open "$CALIBRE_URL" >/dev/null 2>&1 &
else
    log "❌ Error when trying to synchronize, if you're not home, have you verified your VPN is enabled ? (code $STATUS)."
    exit $STATUS
fi
