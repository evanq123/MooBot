import discord

def create_embed(title, text, colour):
    emb = (discord.Embed(description=text, colour=colour))
    emb.set_author(name=title)
    return emb
