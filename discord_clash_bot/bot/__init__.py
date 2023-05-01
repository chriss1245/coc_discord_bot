"""
Bot of the discord_clash_bot package.
"""

import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
