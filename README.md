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
6. Set correct config values in file `solvek.cfg`

# Run server

`python3 pserver.py`

# Update sources

`git pull`

# Libraries

 - [ConfigParser](https://docs.python.org/3/library/configparser.html)
