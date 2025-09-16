#!/bin/bash

# you must test first 
# - your SSH access
# - Calibre URL 

# === Config ===
DEVICE_MOUNT="/media/$USER/KOBOeReader" # mount point here, change for the right one (plug the eReader to check that path)
TARGET_DIR="/srv/dev-disk-by-uuid-f3638c32-4075-40dc-b4e9-abb2d19be252/backups/kobo-rsync" #target of the rsync on the remote NAS
CALIBRE_URL="https://172.22.2.222:8181/" # change it for your calibre linuxserver URL

SSH_USER="helene"
SSH_HOST="OMV-HELENE" #real hostname or host defined in ssh client config (/.ssh/config)

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
