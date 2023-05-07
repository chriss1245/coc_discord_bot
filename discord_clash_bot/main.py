"""
Clash of clans bot
"""
import asyncio

from discord.ext.commands import Bot
import discord
from discord_clash_bot.utils.config import SECRETS

from discord_clash_bot.cogs.admin import AdminCog

async def run():
    """
    Main function
    """

    intents = discord.Intents.all()

    bot = Bot(command_prefix=SECRETS["discord"]["prefix"],
            description="Clash of Clans bot", case_insensitive=True,
            intents=intents)

    cogs = [
        AdminCog
    ]

    for cog in cogs:
        await bot.add_cog(cog(bot))

    await bot.start(SECRETS["discord"]["token"])

if __name__ == "__main__":
    asyncio.run(run())
