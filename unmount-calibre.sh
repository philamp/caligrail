#!/bin/bash

# === Config ===
cd "$(dirname "$0")"
. open-calibre.env

# === Fonctions ===
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# === Vérification du montage Kobo ===
if mountpoint -q "$DEVICE_MOUNT"; then
    if [ -d "$DEVICE_MOUNT/.kobo" ]; then
        log "✅ Kobo détectée sur $DEVICE_MOUNT"
    else
        log "⚠️ Kobo montée mais répertoire .kobo manquant"
        exit 1
    fi
else
    log "❌ Kobo non montée à $DEVICE_MOUNT"
    exit 1
fi

# === Rsync (NAS -> Kobo) ===
log "🚀 Synchronisation NAS -> Kobo ..."
rsync -rtvh --progress --delete -e ssh "$SSH_USER@$SSH_HOST:$TARGET_DIR/" "$DEVICE_MOUNT/"
STATUS=$?

if [ $STATUS -eq 0 ]; then
    log "✅ Synchronisation terminée avec succès."
else
    log "❌ Erreur pendant la synchronisation (code $STATUS)."
    exit $STATUS
fi

# === Démonter la Kobo proprement ===
log "💾 Déconnexion de la Kobo..."
umount "$DEVICE_MOUNT"
if [ $? -eq 0 ]; then
    log "✅ Kobo démontée."
else
    log "⚠️ Impossible de démonter $DEVICE_MOUNT, peut-être encore utilisé."
fi
