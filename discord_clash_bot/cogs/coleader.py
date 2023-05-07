"""
Cog for leader and coleader commands and events
"""

from discord.ext import commands

from discord_clash_bot.api.coc import CocClient

from .base import BaseCog

class ColeaderCog(BaseCog):
    """
    Cog for leader and coleader commands and events
    """

    def __init__(self, bot):
        self.bot = bot
        self.coc_client = CocClient()

    @commands.command()
    @commands.has_role("coleader")
    async def ping(self, ctx):
        """
        Ping the bot
        """
        await ctx.send(f"pong coleader{ctx.author.mention}")
    