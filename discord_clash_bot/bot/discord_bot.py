from . import bot
from . import bot, commands

from .constants import *

import discord

from discord_clash_bot.db import db

#-------------------------General Purpose Commands-------------------------#

@bot.command()
async def ping(ctx):
    """
    Ping the bot
    """
    await ctx.send("pong")

@bot.command()
async def setup(ctx, nickname):
    """
    Setup the user with the given nickname
    """
    # check if the user is in the clan
    # if yes, write welcome to the clan, you are now a member of the clan
    # and give the member the member role
    # if not write this user is not recognized, try again

    if nickname == "test":
        await ctx.send("Welcome to the clan, you are now a member of the clan")
        # give the member the member role
        role = discord.utils.get(ctx.guild.roles, name="member")
        await ctx.author.add_roles(role)

        #change the nickname of the member
        await ctx.author.edit(nick=nickname)
    else:
        await ctx.send("This nickname is not recognized, please try again\n" + \
        "Please enter your Clash of Clans nickname using the following command:\n" + \
        "```!setup <your nickname>``` \n or" + \
        "Please enter your Clash of Clans tag using the following command:\n" + \
        "```!setup_tag <your tag>```")

@bot.command()
async def setup_tag(ctx, tag):
    """
    Setup the user with the given tag
    """
    # check if the user is in the clan
    # if yes, write welcome to the clan, you are now a member of the clan
    # and give the member the member role
    # if not write this user is not recognized, try again

    if tag == "test":
        await ctx.send("Welcome to the clan, you are now a member of the clan")
        # give the member the member role
        role = discord.utils.get(ctx.guild.roles, name="member")
        await ctx.author.add_roles(role)

        #change the nickname of the member
        await ctx.author.edit(nick=tag)
    else:
        await ctx.send("This tag is not recognized, please try again\n" + \
        "Please enter your Clash of Clans nickname using the following command:\n" + \
        "```!setup <your nickname>``` \n or" + \
        "Please enter your Clash of Clans tag using the following command:\n" + \
        "```!setup_tag <your tag>```")

@bot.command()
async def leave(ctx):
    """
    Leave the clan
    """
    # check if the user is in the clan
    # if yes, write you have left the clan
    # and remove the member role
    # if not write you are not in the clan
    await ctx.send(f"{ctx.author.mention} has left the clan")

    # remove the member role
    role = discord.utils.get(ctx.guild.roles, name="member")
    await ctx.author.remove_roles(role)

#-------------------------Role Commands-------------------------#
@bot.command()
@commands.has_role("co-leader")
async def add_role(ctx, role: discord.Role, member: discord.Member):
    """
    Add a role to a member
    """
    await member.add_roles(role)
    await ctx.send(f"{member.mention} has been given the {role.mention} role")


#-------------------------Admin Commands-------------------------#
@bot.command()
@commands.has_permissions(administrator=True)
async def clear_all(ctx, amount=10):
    """
    Clear messages
    """
    await ctx.channel.purge(limit=amount)

#-------------------------Events-------------------------#
@bot.event
async def on_ready():
    """
    Bot is ready
    """
    print("I am ready!")

@bot.event
async def on_member_join(member):
    """
    Write in the welcome channel when a member joins
    """
    # get channel by name
    channel = discord.utils.get(member.guild.channels, name="welcome")
    await channel.send(f"Welcome {member.mention}!\n" + \
        "Please enter your Clash of Clans nickname using the following command:\n" + \
        "```!setup <your nickname>```")

    # ask for the username of the member and check if it is in the clan
    # if not write this user is not recognized, try again
    # if yes, write welcome to the clan, you are now a member of the clan
    # and give the member the member role

   
#-------------------------Error Handling-------------------------#
@bot.event
async def on_command_error(ctx, error):
    """
    Handle errors
    """
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all required arguments")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to run this command")
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send("Role not found")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found")
    else:
        await ctx.send("Something went wrong")

    

# -------------------------Bot-------------------------#
class MyBot:
    """
    Discord bot
    """

    def __init__(self, token):
        self.token = token
        self.bot = bot

    def run(self):
        """
        Run the bot
        """
        self.bot.run(self.token)