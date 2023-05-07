"""
Hanldes interactions with foreigners. The default role a person gets
"""

from .base import BaseCog

from discord.ext import commands

from discord_clash_bot.utils.logging import get_logger

ALLOWED_ROLES = ["foreigner"]
logger = get_logger(__name__)

class ForeignerCog(BaseCog):
    """
    Cog for handling interactions with foreigners. The default role
    a person gets when joins the server.
    """

    # when a new person joins the server, give them the default role
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        When a new person joins the server, give them the default role
        """

        logger.info(f"New member {member} joined the server")
        role = member.guild.get_role("foreigner")
        await member.add_roles(role)

    # when a person leaves the server, remove the default role
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        When a person leaves the server, remove the default role
        """

        logger.info(f"Member {member} left the server")
        role = member.guild.get_role("foreigner")
        await member.remove_roles(role)



    