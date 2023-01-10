# Solvek Smart Server

Personal server which runs on a Raspberry Pi.
Has such features:

1. Telegram bot for misc functions
2. Tracking electricity availability
   1. Logging
   2. Notifying via telegram bot

# Installation

1. If git not installed `sudo apt install git`
2. `git clone https://github.com/solvek/sss.git`
3. `cd sss`
4. `pip3 install -r requirements.txt` [More info](https://note.nkmk.me/en/python-pip-install-requirements/)
5. Create config file `cp solvek.cfg.sample solvek.cfg`
6. Set correct config values in file `nano solvek.cfg`

# Run server

`python3 pserver.py`

# Update sources

`git pull`

# Service

## Adding service

```
sudo touch /etc/systemd/system/pserver.service
sudo nano /etc/systemd/system/pserver.service
```

### File content

```commandline
[Unit]
Description=Petrushky Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=pi
Restart=always
RestartSec=1
ExecStart=python3 /home/pi/sss/pserver.py

[Install]
WantedBy=multi-user.target
```
```
sudo systemctl start pserver
sudo systemctl enable pserver
```

## View service status

`sudo systemctl status pserver`

### View logs

`journalctl --unit=pserver.service -n 100 --no-pager`

#### Restart logging (this clears logs)

`systemctl restart systemd-journald`

## Stop service

`sudo systemctl stop pserver`

## Restart service

```
systemctl daemon-reload
systemctl restart pserver
```

## Remove service

```
sudo systemctl stop pserver
sudo systemctl disable pserver
```

# Storing locally data in csv

```commandline
nano blackouts.csv
```

# GPIO Command line

```commandline
raspi-gpio set 17 ip pu
raspi-gpio get 17
```

## Wiring

 - Yellow - ground
 - Red - GPIO17

# Telegram bot commands

 - `/light_pause`
 - `/light_resume`
 - `/command <command>`
 - `/cchmod` - permissions for usb directory content
 - `/clogs` - view pserver logs

## Deluge commands

 - `/deluge info` - list torrents
 - `/deluge rm <torrent-id>` - remove torrent
 - `/deluge add <magnet>` - add torrent by [magnet](https://nutbread.github.io/t2m/)

# Libraries

 - [ConfigParser](https://docs.python.org/3/library/configparser.html)
