"""
cli commands
"""

import asyncio
import os
import signal
import click

from discord_clash_bot.utils.logging import get_logger
from discord_clash_bot.utils.config import PROJECT_DIR

logger = get_logger(__name__)
pid_file = PROJECT_DIR / "discord_clash_bot.pid"

@click.group()
@click.pass_context
def cli(ctx):
    """
    Discord clash bot cli
    """
    ctx.ensure_object(dict)

@cli.command()
def run():
    """
    Run the bot
    """
    from discord_clash_bot import main

    if pid_file.exists():
        logger.error("Bot already running")
        return

    with open(pid_file, "w", encoding="utf-8") as pid:
        pid.write(str(os.getpid()))

    try:
        logger.info("Starting bot")
        asyncio.run(main.run())
    except KeyboardInterrupt:
        logger.info("Stopping bot")
        pid_file.unlink()

@cli.command()
def stop():
    """
    Stop the bot, if it is running. If the bot is not running, just delete the pid file.
    """
    if not pid_file.exists():
        logger.error("Bot not running")
        logger.debug(f"Not found {pid_file}, bot may be daemonized")
        return

    with open(pid_file, "r", encoding="utf-8") as pid:
        pid = int(pid.read())
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        logger.warning("Bot not running, deleting just pid record")

    pid_file.unlink()
    logger.info("Bot stopped")

@cli.command()
def restart():
    """
    Restart the bot
    """
    stop()
    run()
