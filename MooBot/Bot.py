import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.voice_client import VoiceClient

description = '''
MooBot is developed by Evan Quach using Python and the discord.py api
to be used exclusively by Koot for server maintanence and as a local
music player.
---------------------------------------------------------------------
(Last updated: 2012.12.22 v0.01a)

KNOWN BUGS:
-   Documentation and "help" are unfinished.
-   'Purge' cannot bulk delete over 100 messages
    and/or messages that over 14 days old.
    (TEMPFIX): Messages are slowly deleted 1 at a time.
-   Music.py work in progress.
'''

startup_extensions = ["Music"] #Music cog
Client = discord.Client()
bot = commands.Bot(command_prefix = "!", description = description)
Token = "MzIyMTE1ODU3MTQ2ODM5MDUx.DR53-g.e8Xqsvk27JXMbISeGjuVPopAId0"

@bot.event
async def on_ready():
    print("MooBot is running...")
    print("--------------------")
@bot.command(pass_context = True)
async def test(ctx):
    await bot.say("{} MooBot is running!".format(ctx.message.author.mention))

@bot.command(pass_context = True)
async def purge(ctx, number):
    number = int(number) + 1 #ignores the context message
    mgs = []
    try:
        async for x in bot.logs_from(ctx.message.channel, limit = number):
            mgs.append(x)
        await bot.delete_messages(mgs)
    except:
        await bot.say("Attempting to delete 1 message at a time")
        await asyncio.sleep(5.0)
        number += 1
        counter = 0
        async for x in bot.logs_from(ctx.message.channel, limit = number):
            if counter < number:
                await bot.delete_message(x)
                counter += 1
                await asyncio.sleep(1.2)

@bot.async_event
async def on_message(message):
    author = message.author
    if "Austin" in message.content:
        boaustinID = '<@204635243041259521>'
        await bot.send_message(message.channel, "{} Onii sama, {} is calling you.".format(boaustinID, author.mention))




bot.run(Token)
