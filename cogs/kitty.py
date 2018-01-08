from discord.ext import commands
import aiohttp
import functools
import asyncio


GIPHY_API_KEY = "dc6zaTOxFJmzC"


class Kitty:
    """Kitty related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=False, no_pm=True)
    async def kitty(self):
        """Searches for random cute sleeping kitties on giphy."""
        tag = "cute+sleeping+kitties"
        url = ("http://api.giphy.com/v1/gifs/random?&api_key={}&tag={}"
               "".format(GIPHY_API_KEY, tag))

        async with aiohttp.get(url) as r:
            result = await r.json()
            if r.status == 200:
                if result["data"]:
                    await self.bot.say(result["data"]["url"])
                else:
                    await self.bot.say("No results found.")
            else:
                await self.bot.say("Error contacting the API")


def setup(bot):
    bot.add_cog(Kitty(bot))
