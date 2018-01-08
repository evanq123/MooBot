from discord.ext import commands
import functools
import asyncio

try:
    from imgurpython import ImgurClient
except:
    ImgurClient = False

CLIENT_ID = "1fd3ef04daf8cab"
CLIENT_SECRET = "f963e574e8e3c17993c933af4f0522e1dc01e230"


class Kitty:
    """Kitty related commands."""

    def __init__(self, bot):
        self.bot = bot
        self.imgur = ImgurClient(CLIENT_ID, CLIENT_SECRET)

    @_imgur.command(pass_context=True, name="subreddit")
    async def aww(self, ctx, subreddit="aww", sort_type: str="top", window: str="day"):
        """Gets gif from the /r/aww subreddit section"""
        links = []

        task = functools.partial(self.imgur.subreddit_gallery, subreddit,
                                 sort=sort, window=window, page=0)
        task = self.bot.loop.run_in_executor(None, task)
        try:
            items = await asyncio.wait_for(task, timeout=10)
        except asyncio.TimeoutError:
            await self.bot.say("Error: request timed out")
            return

        for item in items[:1]:  # Can be changed
            link = item.gifv if hasattr(item, "gifv") else item.link
            links.append("{}\n{}".format(item.title, link))

        if links:
            await self.bot.say("\n".join(links))
        else:
            await self.bot.say("No results found.")


def setup(bot):
    if ImgurClient is False:
        raise RuntimeError("You need the imgurpython module to use this.\n"
                           "pip3 install imgurpython")

    bot.add_cog(Kitty(bot))
