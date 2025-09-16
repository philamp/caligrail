# caligrail for kobo
Plug your local USB eReader to a remote Calibre instance

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

- (ubuntu) right click on .desktop files "allow launching"

- `open-calibre.sh` to start the upstream sync (eReader to Calibre and start the web browser to open Calibre)

- when Calibre is open, use the connect to folder itme and choose `/mnt/kobo` + the kobo that is emulated

- `unmount-calibre.sh` to start the downstream sync (Calibre to eReader and unmount the USB eReader)



- create a custom field named "collec"

- use import.py -> use it with `calibre-debug -e` inside the container (TODO)


## TODOs

- TODO configure an automatic collection in kobotouch ...
- TODO addon to auto put books in kobo based on criterias
- TODO install cron for import script
- TODO start stop docker to avoid any ambiguity
- TODO rsync should not be possible if calibre is alive
  - force user to close calibre in order to sync back ??
- TODO to start, loop until it's mounted
- permissions upstream downstream 

