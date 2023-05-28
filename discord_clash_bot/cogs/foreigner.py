"""
Handles the interactions with foreigners. When a new person joins the server,
they are given the default role for foreigners. They can then setup their
membership using the !setup command.

"""

import discord
from discord.ext import commands
from discord_clash_bot.api.coc import CocClient
from discord_clash_bot.utils.config import PROJECT_DIR, SECRETS
from discord_clash_bot.utils.logging import get_logger

# false positive from pylint
# pylint: disable=relative-beyond-top-level
from .base_cog import BaseCog


logger = get_logger(__name__)

coc = CocClient(SECRETS["coc"]["token"])


class DMCog(BaseCog):
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

        # send a private message to the new member to setup their account
        await member.send(f"Welcome {member} to {member.guild.name}!")
        setup_msg = (
            "To setup you in the clan and get access to the server, "
            + "please send me your clash of clans nickname and your "
            + "verification token, which can be found in settings/more setting/api_token"
            + " in the clash of clans app."
        )

        await member.send(setup_msg)
        # send images with instructions

        img_path = PROJECT_DIR / "discord_clash_bot/media/setup/more_settings.jpeg"

        with open(img_path, "rb") as img:
            await member.send(file=discord.File(img))

        img_path = PROJECT_DIR / "discord_clash_bot/media/setup/copy_token.jpeg"
        with open(img_path, "rb") as img:
            await member.send(file=discord.File(img))

        instruc_msg = (
            "Once you have that, you can setup your membership"
            + "using one of the following commands:\n"
            + "`!setup my_nickname my_token` i.e. `!setup carlitos 12345678sa` or\n"
            + "`!setup_tag my_tag my_token` i.e. `!setup_tag #1DSAsqwr 1234dsf7890`\n"
            + "MAKE THE SETUP THROUGH A PRIVATE MESSAGE. DO NOT SEND THE COMMANDS IN THE SERVER"
        )

        await member.send(instruc_msg)

    # when a person leaves the server, remove the default role
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        When a person leaves the server, remove the default role
        """

        logger.info(f"Member {member} left the server")
        role = member.guild.get_role("foreigner")
        await member.remove_roles(role)

    # setup the member in the clan
    @commands.command()
    async def setup(self, ctx, nickname, token):
        """
        Makes sure that the user exist in the clan and that the token is valid
        """

        members = coc.get_clan_members(SECRETS["coc"]["clan_tag"])

        for member in members:
            if member["name"] == nickname:
                response = coc.post_verify_player(member["tag"], token)
                if response["status"] == "valid":
                    # add the member to the clan
                    role = member["role"]
                    if role == "admin":
                        role = "elder"

                    await ctx.author.add_roles(ctx.guild.get_role(role))
                    await ctx.author.remove_roles(ctx.guild.get_role("foreigner"))
                    # set as nickname the clash of clans nickname
                    await ctx.author.edit(nick=nickname)
                    await ctx.send(
                        f"Success: welcome {ctx.author} to the clan! You are now a {role}"
                    )
                    # write in general chat that a new member joined the clan
                    general_chat = ctx.guild.get_channel("general")
                    await general_chat.send(f"Welcome {ctx.author} to the clan!")
                    return

        await ctx.send("Error: nickname or token invalid. Please try again")
