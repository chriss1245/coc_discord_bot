"""
Cogs for admin commands and events
"""


from discord.ext import commands
from discord.member import Member
from discord_clash_bot.api.coc import CocClient
from discord_clash_bot.utils.logging import get_logger

# false positive from pylint
# pylint: disable=relative-beyond-top-level
from .base_cog import BaseCog, Role

ALLOWED_ROLES = [Role.ADMIN.value]
logger = get_logger(__name__)


class AdminCog(BaseCog):
    """
    Cog for admin commands and events
    """

    allowed_roles = ALLOWED_ROLES
    __cog_name__ = "Admin"

    def __init__(self, bot):
        self.bot = bot
        self.coc_client = CocClient()

    def cog_check(self, ctx: commands.Context) -> bool:
        """
        Makes sure that the user is using the command in a guild and has the
        correct role to use the command. This is the only cog which allows DM with
        the bot.
        """

        # check that the user is talking in a guild (it is a member)
        if isinstance(ctx.author, Member):
            return any(role.name in self.allowed_roles for role in ctx.author.roles)

        return ctx.author.id in self.bot.owner_ids

    # when the bot joins a server, message the owner to setup the bot
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        When the bot joins a server, message the owner to setup the bot
        """
        logger.info(f"Joined new guild {guild.name}")
        await guild.owner.send(
            f"Thanks for adding me to {guild.name}! Please use the !setup_discord command to setup the bot."
            + "\nTake into account that setting up the bot involves, creating roles, channels and permissions."
            + "\nIf you have any questions, please contact the bot owner."
        )

    # TODO: add a command to setup the bot in a server
    @commands.command()
    async def setup_bot(self, ctx):
        """
        Setup the bot in the server. This command should be used in DM with the bot.

        Creates the roles, channels and permissions for the bot to work.
        """

        if isinstance(ctx.author, Member):
            await ctx.send(
                "This command should be used in DM with the bot. Please send me a DM."
            )
