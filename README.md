# Discord BDO Roles Bot #
This bot allows members of the server to receive roles for the various bosses as well as Imperial Cooking and Crafting in BDO.


## Install ##
### Python ###
This bot was developed with Python 3.8.5.

### Install the Discord library ###

`pip install discord`

### Configuration ###
Rename the **config.example.py** to **config.py** and enter your discord bot token after 'discord_token'.

### BDO Timers ###
The main reason for this bot is to give members the roles so that the "BDO Timers" bot can mention them when an appropriate event occurs. If you are not using the "BDO Timers" bot, set the corresponding line in the configuration to false!

You can find the BDO Timers Bot [here](https://kirtash.gitbook.io/bdotimers/).

### Start the bot ###
To start the bot, simply enter

`python3 main.py`

### Using the bot ###
After you've started the bot and added it to your server, you can start using it by simply typing ``!initBdoRoles`` in any channel. 
The bot must have read and write permissions for this channel! The bot then deletes your message and sends the role-assignment interface.

### Setting up on debian 10 with autostart ###
#### Install Python and pip ####

`apt install python3-pip`

#### Create new User and the directories for the bot ####

```
useradd -r -s /bin/false bdorolesbot`
mkdir /etc/bdoRolesBot
chown -R bdorolesbot:bdorolesbot /etc/bdoRolesBot/
```

#### Enable autostart ####
Create a new service file:

`nano /etc/systemd/system/bdorolesbot.service`

Content of this file:

```shell script
#!/bin/bash
[Unit]
Description=BDO Roles Discord Bot
After=syslog.target

[Service]
Type=simple
User=bdorolesbot
Group=bdorolesbot
WorkingDirectory=/etc/bdoRolesBot
ExecStart=python3 /etc/bdoRolesBot/main.py
SyslogIdentifier=bdorolesbot
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

If you change something on this file, reload the daemon to apply the changes:

`systemctl daemon-reload`

Enable and start the service:
```
systemctl enable bdorolesbot.service
systemctl start bdorolesbot.service
```

To check the status: 

`systemctl status bdorolesbot.service`