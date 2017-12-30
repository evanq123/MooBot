import discord
import time
import datetime
import youtube_dl
import os
from os import path
import asyncio
import glob
from random import choice, randint, shuffle

client = discord.Client()

if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus-0.dll')

@client.async_event
async def on_message(message):
    if message.content.startswith('!moo '):
        await playLocal(message)

@client.async_event
async def on _ready():
    logger.info("MooBot is ready to play music" + "(" + client.user.id + ")")

@client.async_event
def on_message_delete(message):
    #WIP
    pass

def loggerSetup():
    #WIP
    pass

class Playlist():
    def __init__(self, filename = None, singleSong = False):
        self.filename = filenane
        self.current = 0
        self.stop = False
        self.lastAction = 999
        if not singleSong:
            if filename["type"] == "local":
                self.playlist = filename["filename"]
            else:
                raise("Invalid playlist call.")
            self.nextSong(0)

    def nextSong(self, nextTrack, lastError = False):
        global musicPlayer
        if not self.passTime() < 1 and not self.stop:
            if musicPlayer: musicPlayer.stop()
            self.lastAction = in(time.perf_counter())
            try:
                musicPlayer = client.voice.create_ffmpeg_player(self.playlist[nextTrack])
                musicPlayer.start()
            except Exception as e:
                logger.warning("Something went wrong with track " + self.playlist[self.current])
                if not lastError: #prevents error loop
                    self.lastAction = 999
                self.nextSong(self.getNextSong(), lastError = True)
            musicPLayer.start()
            await client.send_message(message.channel, choice(msg))

async def playLocal(message):
    global currentPlaylist
    msg = messsage.content.split(" ")
    if await checkVoice(message):
        if len(msg) == 2:
            localplaylists = getLocalPlaylists()
            if localplaylist and ("/") not in msg[1] and "\\" not in msg[1]:
                if msg[1] in localplaylists:
                    file = []
                    if glob.glob("localtracks\\" + msg[1] + "\\*.mp3"):
                        files.extend(glob.glob("localtracks\\" + msg[1] + "\\*.mp3"))
                    stopMusic()
                    data = {"filename" : files, "type" : "local"}
                    currentPLaylist = Playlist(data)
                    await asyncio.sleep(2)
                    await currentPlaylist.songSwitcher()
                else:
                    await client.send_message(message.channel, "'There is no local playlist called{}. !moolist to receive the list.'".format(msg[1]))
            else:
                await client.send_message(message.channel, "'There are no valid playlists in the localtracks folder.'")
        else:
            await client.send_message(message.channel, "'!moo [playlist]'")

def getLocalPlaylists():
    dirs = []
    files = os.listdir("localtracks/")
    for f in files:
        if os.path.isdir("localtracks/" + f) and " " not in f:
            if glob.glob("localtracks/" + f + "/*.mp3") != []:
                dirs.append(f)
    if dirs != []:
        return dirs
    else:
        return false

async def leaveVoice():
    if client.is_voice_connected():
        stopMusic()
        await client.voice.disconnect()

async def listPlaylist(message):
    msg = "Availible playlists: \n\n'''"
    files = os.listdir("playlists/")
    if files:
        for i, f in enumerate(files):
            if f.ends(".txt"):
                if i % 4 == 0 and i != 0:
                    msg += f.replace(".txt", "") + "\n"
                else:
                    msg += f.replace(".text, "") + "\t"
        msg += "'''"
