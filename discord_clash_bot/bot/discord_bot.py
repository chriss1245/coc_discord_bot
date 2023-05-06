"""
Discord bot for the Clash of Clans. Interface with
for commands and events
"""

from . import bot
from . import bot, commands
import traceback

import toml
from pathlib import Path

from discord_clash_bot.api.coc_wrapper import CocClient

import discord

from discord_clash_bot.db.db import DBConnection



secrets = toml.load(Path().cwd() / "secrets.toml")


db = DBConnection(secrets["db"]["url"])
coc = CocClient(secrets["coc"]["token"])
clan_tag = secrets["coc"]["clan"]
#-------------------------General Purpose Commands-------------------------#

@bot.command()
async def setup(ctx, nickname):
    """
    Setup the user with the given nickname
    """
    # check if the user is in the clan
    # if yes, write welcome to the clan, you are now a member of the clan
    # and give the member the member role
    # if not write this user is not recognized, try again
    members = coc.get_clan_members(clan_tag)
    member_names = [member.name for member in members]
    if nickname in member_names:
        await ctx.send("Welcome to the clan, you are now a member of the clan")
        # give the member the member role
        # get the role of the member
        member = members[member_names.index(nickname)]
        # convert to lower case
        role_name = member.role.lower()
        await ctx.send("Your role is: " + role_name)
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        await ctx.author.add_roles(role)

        #remove foreigner role
        foreigner_role = discord.utils.get(ctx.guild.roles, name="foreigner")
        await ctx.author.remove_roles(foreigner_role)

        #change the nickname of the member
        await ctx.author.edit(nick=nickname)
    else:
        await ctx.send("This nickname is not recognized, please try again\n" + \
        "Please enter your Clash of Clans nickname using the following command:\n" + \
        "```!setup <your nickname>``` \n or" + \
        "Please enter your Clash of Clans tag using the following command:\n" + \
        "```!setup_tag <#your tag>```")

@bot.command()
async def setup_tag(ctx, tag):
    """
    Setup the user with the given tag
    """
    # check if the user is in the clan
    # if yes, write welcome to the clan, you are now a member of the clan
    # and give the member the member role
    # if not write this user is not recognized, try again

    members = coc.get_clan_members(clan_tag)
    member_tags = [member.tag for member in members]
    if tag in member_tags:
        # get the nickname of the member
        member = members[member_tags.index(tag)]
        nickname = member.name
        role_name = member.role.lower()

        # get the role of the member
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        await ctx.send("Welcome to the clan, you are now a member of the clan")
        await ctx.author.add_roles(role)

        #remove foreigner role
        foreigner_role = discord.utils.get(ctx.guild.roles, name="foreigner")
        await ctx.author.remove_roles(foreigner_role)

        #change the nickname of the member
        await ctx.author.edit(nick=nickname)
    else:
        await ctx.send("This tag is not recognized, please try again\n" + \
        "Please enter your Clash of Clans nickname using the following command:\n" + \
        "```!setup <your nickname>``` \n or" + \
        "Please enter your Clash of Clans tag using the following command:\n" + \
        "```!setup_tag <#your tag>```")

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
    # remove all the roles of the member
    for role in ctx.author.roles:

        # remove all roles except @everyone
        if role.name != "@everyone":
            await ctx.author.remove_roles(role)
        
    # add the foreigner role
    foreigner_role = discord.utils.get(ctx.guild.roles, name="foreigner")
    await ctx.author.add_roles(foreigner_role)



#-------------------------Role Commands-------------------------#
@bot.command()
@commands.has_role("coleader")
async def add_role(ctx, role: discord.Role, member: discord.Member):
    """
    Add a role to a member
    """
    await member.add_roles(role)
    await ctx.send(f"{member.mention} has been given the {role.mention} role")

@bot.command()
async def kick_out(ctx, member: discord.Member, reason: str = None):
    """
    Kick out a member
    """

    if ctx.author.top_role < member.top_role:
        await ctx.send("You cannot kick out this member")
        return
    await member.kick()

    # write in general that the member has been kicked out
    await ctx.send(f"{member.mention} has been kicked out of the clan")


#-------------------------Admin Commands-------------------------#
@bot.command()
@commands.has_permissions(administrator=True)
async def clear_all(ctx, amount=10):
    """
    Clear messages
    """
    await ctx.channel.purge(limit=amount)

@bot.command()
@commands.has_permissions(administrator=True)
async def create_db(ctx):
    """
    Create the database
    """
    db.create_all()

    await ctx.send("Database created")


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

    # remove channel content if it is not empty
    channel = discord.utils.get(member.guild.channels, name="welcome")
    await channel.purge()


    # give foreigner role
    role = discord.utils.get(member.guild.roles, name="foreigner")
    await member.add_roles(role)

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
        # check that the author is admin and the channel is debug

        # get the debug channel
        channel = discord.utils.get(ctx.guild.channels, name="debug")
        trace = traceback.format_exception(type(error), error, error.__traceback__)
        # print used command, author and channel
        await channel.send("Command: " + str(ctx.command))
        await channel.send("Author: " + str(ctx.author))
        await channel.send("Channel: " + str(ctx.channel))

        await channel.send("Something went wrong: " + str(error))
        await channel.send("".join(trace))
        await ctx.send("Unknown error ocurred. Try again later or contact the admin")


    

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