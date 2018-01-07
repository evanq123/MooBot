# MooBot - A Modular Discord bot
#### *Plays local music files and has general purpose server utilities*
[<img src="https://img.shields.io/badge/discord-py-blue.svg">](https://github.com/Rapptz/discord.py) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

**MooBot** is a fully modular bot – meaning all features and commands can be enabled/disabled to your liking, making it completely customizable. This is a *self-hosted bot*.

The default set of cogs are:
* Moderation features
* Music features

# TODO:
**audio.py:**
* Play .mp3 files sent to discord.
* (local only) Send a download link for .mp3 file currently playing.
* Send link to lyrics (or fetch).
* Seek (to Time/ +10 secs).
* (local only) Display Album/Anime track belongs to.
* (local only) Display title and artist
* (local only) Display comments in metadata.
* Adding server hosting.

**Other cogs:**
* akinator.py
* steam.py
* league.py

# Installation

WIP

# Known Bugs
**audio.py:**
* Fix duration (1:00) for songs over 1:00

**mod.py:**
* !cleanup does not function properly.

Needs more testing:
* !rename on normal users.
* filtered words on normal users.
# License

Released under the [GNU GPL v3](LICENSE).
