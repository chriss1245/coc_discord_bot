"""
cli commands
"""

import click
import toml

from discord_clash_bot.bot.discord_bot import MyBot
from discord_clash_bot.api.coc_wrapper import CocClient
from discord_clash_bot.db.db import DBConnection

@click.group()
@click.pass_context
@click.option("--secrets", "-s", type=click.Path(exists=True), required=True, default="secrets.toml")
def cli(ctx, secrets):
    ctx.ensure_object(dict)

    with open(secrets, "r", encoding="utf-8") as f:
        secrets = toml.load(f)
    ctx.obj["secrets"] = secrets

@cli.command()
@click.pass_context
def run(ctx):
    """
    Run the bot
    """
    token = ctx.obj["secrets"]["discord"]["token"]
    bot = MyBot(token)
    bot.run()
