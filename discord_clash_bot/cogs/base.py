"""
Base discord cog class. Implements basic events
and handles permissions based on roles
"""
#TODO error handling

from discord.ext import commands

class BaseCog(commands.Cog):
    """
    Base discord bot cog class
    """
    @commands.Cog.listener()
    async def on_ready(self):
        """
        Cog is ready
        """
        print(f"{self.__class__.__name__} has been loaded.")

    @commands.Cog.listener()
    async def on_unload(self):
        """
        Cog is unloaded from the bot
        """
        print(f"{self.__class__.__name__} has been unloaded.")
