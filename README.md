# MooBot.v1 - A Modular Discord bot
#### THIS VERSION IS NO LONGER SUPPORTED
#### *Plays local music files and has general purpose server utilities*
[<img src="https://img.shields.io/badge/discord-py-blue.svg">](https://github.com/Rapptz/discord.py) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

**MooBot** is a fully modular bot – meaning all features and commands can be enabled/disabled to your liking, making it completely customizable. This is a *self-hosted bot*.

The default set of cogs are:
* Moderation features
* Music features

**audio.py:**
* Play .mp3 files sent to discord.
* Send link to lyrics (or fetch).
* Seek (to Time/ +10 secs).
* (local only) Send a download link for .mp3 file currently playing.
* (local only) Display Album/Anime track belongs to.
* (local only) Display title and artist.
* (local only) Display comments in metadata.
* Adding server hosting.

**Ideas for cogs:**
* akinator.py
* steam.py
* league.py
* overwatch.py

# Getting Started:
## CentOS 7:
### Installing the pre-requirements
```
yum -y groupinstall development
yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum -y install yum-utils wget which python35u python35u-pip python35u-devel openssl-devel libffi-devel git opus-devel
sh -c "$(wget https://gist.githubusercontent.com/mustafaturan/7053900/raw/27f4c8bad3ee2bb0027a1a52dc8501bf1e53b270/latest-ffmpeg-centos6.sh -O -)"
```
### Cloning the bot
```
git clone -b v1-develop --single-branch https://github.com/evanq123/MooBot.git
```
### Updating the bot requirements
```
cd MooBot
python3.5 launcher.py
```
From there select Install requirements and select 1 or 2

## Creating a bot account
WIP

## Running the bot
Enter the bot directory and start the launcher, then select option 1 or 2 and follow the initial setup.
```
python3.5 launcher.py
```

## Updating the bot
To update the bot enter the bot directory and start the launcher, then select Update and select 1, 2, or 3
```
python3.5 launcher.py
```

## License
Released under the [GNU GPL v3](LICENSE).
