# caligrail
Plug your local USB eReader to a remote Calibre instance

## Prerequisites
- A linux laptop (windows version maybe later)
- A NAS with https://hub.docker.com/r/linuxserver/calibre with PUID and GUID configured with of SSH user
- rsync on Laptop and NAS

## Files
`open-calibre.sh` to start the upstream sync (eReader to Calibre and start the web browser to open Calibre)

`unmount-calibre.sh` to start the downstream sync (Calibre to eReader and unmount the USB eReader)

`chmod +x *.sh`to be able to run the scripts


## Bonuses

### configure Kobotouch to create Collections

### Configure readlist addon to automatically sync based on criterias
