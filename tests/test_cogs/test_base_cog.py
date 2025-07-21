"""
Tests of the base cog functionality
"""

from discord_clash_bot.cogs.base_cog import BaseCog


class MockCog(BaseCog):
    """
    Mock cog for testing
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        """
        Handle errors
        Args:
            ctx: context
            error: error
        """
        raise NotImplementedError("cog_command_error")

    # enforce permissions policy for commands before executing them
    async def cog_before_invoke(self, ctx):
        """
        Check if user has the required role to execute the command
        Args:
            ctx: context
        """

    # enforce a log policy for commands after executing them
    async def cog_after_invoke(self, ctx):
        """
        Log command execution
        Args:
            ctx: context
        """
        raise NotImplementedError
