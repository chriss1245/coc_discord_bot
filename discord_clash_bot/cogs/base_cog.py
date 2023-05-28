"""
Base discord cog class. Implements basic events
and handles permissions based on roles.

All cogs should inherit from this class, and have to implement
the following methods:
"""

from abc import abstractmethod, ABCMeta
from enum import Enum

from discord.ext import commands


class Role(Enum):
    """
    Roles for discord users
    """

    ADMIN = "admin"
    LEADER = "leader"
    COLEADER = "coleader"
    ELDER = "elder"
    MEMBER = "member"
    FOREIGNER = "foreigner"

    def __str__(self):
        return self.value


class CogABCMeta(commands.CogMeta, ABCMeta):
    """Metaclass for cogs that inherit from ABC"""


class BaseCog(commands.Cog, metaclass=CogABCMeta):
    """
    Base discord bot cog class. Implements a basic set of
    policies, and stablishes a contract for all cogs.
    """

    # enforce child methods to implement a error handling policy
    @abstractmethod
    async def cog_command_error(
        self, ctx: commands.Command, error: commands.CommandError
    ) -> None:
        """
        Handle errors, and send a message to the user
        Args:
            ctx: context
            error: error
        """
        raise NotImplementedError

    # enforce permissions policy for commands before executing them
    @abstractmethod
    def cog_check(self, ctx: commands.Context) -> bool:
        """
        Check if user has the required role to execute the command
        Args:
            ctx: context
        """
        raise NotImplementedError

    @commands.command()
    async def ping(self, ctx):
        """
        Ping the bot
        """
        await ctx.send("pong")
