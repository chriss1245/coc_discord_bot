"""
Cogs for admin commands and events
"""

from discord.ext import commands

from discord_clash_bot.api.coc import CocClient

from .base import BaseCog

ALLOWED_ROLES = ["leader"]

class AdminCog(BaseCog):
    """
    Cog for admin commands and events
    """

    def __init__(self, bot):
        self.bot = bot
        self.coc_client = CocClient()

    @commands.command()
    @commands.has_any_role(*ALLOWED_ROLES)
    async def ping(self, ctx):
        """
        Ping the bot
        """
        await ctx.send("pong")
