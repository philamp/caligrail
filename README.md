# caligrail for kobo
Plug your local USB eReader to a remote Calibre instance

## Prerequisites
- A Linux client PC (windows version maybe later)
- create the "kobo-rsync" folder somewhere in the NAS (owned by SSH user in RW)
- A Linux server with https://hub.docker.com/r/linuxserver/calibre with PUID and GUID configured with the SSH user and
  - in docker compose on run, add the mount from the `../kobo-rsync` folder to `/mnt/kobo` (calibre will see it)
- rsync on Laptop and NAS
- create a custom field named "collec"

> [!TIP]
> You can generate a SSH key pair with `ssh-keygen -t ed25519 -C "uremail@exemple.com" -f ~/.ssh/yourkey`
> - it will generate the private key yourkey and the public one `yourkey.pub`
> - put the `yourkey.pub` content in authorized_keys of the connecting user (/home/user/.ssh/authorized_keys)
> - ...and add the user to _ssh or ssh group to allow ssh connection (depends on the OS)

## Files
`open-calibre.sh` to start the upstream sync (eReader to Calibre and start the web browser to open Calibre)

when Calibre is open, use the connect to folder itme and choose `/mnt/kobo` + the kobo that is emulated

`unmount-calibre.sh` to start the downstream sync (Calibre to eReader and unmount the USB eReader)

`chmod +x *.sh`to be able to run the scripts

import.py -> use it with `calibre-debug -e`


## Bonuses

### configure Kobotouch to create Collections

- configure an automatic collection in kobotouch ...

### Configure readlist addon to automatically sync based on criterias
