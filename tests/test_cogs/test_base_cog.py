"""
Tests of the base cog functionality
"""

from unittest.mock import MagicMock, patch, Mock

import unittest

from discord.ext import commands
from discord.ext.commands import Context, CommandError

from discord_clash_bot.cogs.base_cog import BaseCog, Role

from discord.ext import commands


class MockCog(BaseCog):
    """
    Mock cog for testing
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(
        self, ctx: commands.Command, error: commands.CommandError
    ):
        """
        Handle errors
        Args:
            ctx: context
            error: error
        """
        raise Exception("cog_command_error")

    # enforce permissions policy for commands before executing them
    async def cog_before_invoke(self, ctx: commands.Context):
        """
        Check if user has the required role to execute the command
        Args:
            ctx: context
        """

    # enforce a log policy for commands after executing them
    async def cog_after_invoke(self, ctx: commands.Context):
        """
        Log command execution
        Args:
            ctx: context
        """
        raise NotImplementedError
