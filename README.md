# Caligrail for kobo
- Plug your local USB eReader to a remote VNC Calibre instance (not through USB over network but through rsync)
- and automatic sync between a "Shared watched folder" and Calibre library 

This is VERY experimental in its current state

## The current workflow is:

- user puts (licence free) ebook files in a SMB/NFS/whatever watched folder 
- files synced to remote Calibre DB *overnight* 
- (initiated by a bash script) user plugs Kobo into linux laptop and open remote Calibre through VNC session in its browser
- user works in Calibre and "send to device" the books he wants 
- user closes calibre 
- (initiated by a bash script) user syncs to kobo and unmount it

## Prerequisites
- A Linux client PC (windows version maybe later)
- A Linux server w
- rsync on Laptop and NAS


> [!TIP]
> You can generate a SSH key pair with `ssh-keygen -t ed25519 -C "uremail@exemple.com" -f ~/.ssh/yourkey`
> - it will generate the private key yourkey and the public one `yourkey.pub`
> - put the `yourkey.pub` content in authorized_keys of the connecting user (/home/user/.ssh/authorized_keys)
> - ...and add the user to _ssh or ssh group to allow ssh connection (depends on the OS)

## Steps

- create the "kobo-rsync" folder somewhere in the NAS (owned by SSH user in RW)

- use https://hub.docker.com/r/linuxserver/calibre with PUID and GUID configured with the SSH user that will use the scripts
  - in docker compose on run, add the mount from the `../kobo-rsync` folder to `/mnt/kobo` (calibre will see it)

- `open-calibre.env` to put settings

- `chmod +x *.sh`to be able to run the scripts

- (ubuntu) right click on .desktop files "allow launching" if you want to use desktop shortcuts

- `open-calibre.sh` to start the upstream sync (eReader to Calibre and start the web browser to open Calibre)

- when Calibre is open, use the *connect to folder icon* and choose `/mnt/kobo` + choose carefully the kobo that should be emulated

- `unmount-calibre.sh` to start the downstream sync (Calibre to eReader and unmount the USB eReader)

- create a custom field named "collec" and configure kobotouch to use it to create collections in the Kobo db

- use import.py -> use it with `calibre-debug -e` inside the container (TODO nice install)


## TODOs

- TODO explain how to configure an automatic collection in kobotouch
- TODO install cron for import script
- TODO start stop docker to avoid any ambiguity
- TODO rsync should not be possible if calibre is alive
  - force stop container before syncing to NAS
  - restart container after syncing to NAS
  - force user to close calibre in order to sync back to Kobo ??
- TODO start, loop while until eReader is mounted
- permissions upstream downstream check (should be same user as SSH that writes in NAS folder comgin from calibre docker or ssh rsync)

optional:

- TODO is there an addon to auto put books in kobo based on criterias ?
