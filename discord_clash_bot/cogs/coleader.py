"""
Cog for leader and coleader commands and events
"""

from discord.ext import commands

from discord_clash_bot.api.coc import CocClient

# false positive from pylint
# pylint: disable=relative-beyond-top-level
from .base_cog import BaseCog
from .base_cog import Rol


ALLOWED_ROLES = [Rol.LEADER, Rol.COLEADER]


class ColeaderCog(BaseCog):
    """
    Cog for leader and coleader commands and events
    """

    def __init__(self, bot):
        self.bot = bot
        self.coc_client = CocClient()

    def cog_before_invoke(self, ctx: commands.Context):
        """
        Apply permissions policy for commands before executing them
        """
        return self.check_role(ctx, ALLOWED_ROLES)

    @commands.command()
    async def ping(self, ctx):
        """
        Ping the bot
        """
        await ctx.send(f"pong coleader{ctx.author.mention}")
