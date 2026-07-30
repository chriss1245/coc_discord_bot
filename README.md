# Clash of Clans Discord Bot

[![Unit Tests](https://github.com/chriss1245/coc_discord_bot/actions/workflows/test.yml/badge.svg)](https://github.com/chriss1245/coc_discord_bot/actions/workflows/test.yml)
[![Pylint](https://github.com/chriss1245/coc_discord_bot/actions/workflows/norm_checking.yml/badge.svg)](https://github.com/chriss1245/coc_discord_bot/actions/workflows/norm_checking.yml)

A Discord bot that pulls clan and player data from the Clash of Clans API and serves it to
a Discord server.

🌐 **[manapple.dev](https://manapple.dev)** &nbsp;|&nbsp; [en español](https://manapple.dev/es/)

---

## What it is

A side project, built with the same structure I would give a work service — because the
habit is the point. It is a packaged Python application rather than a single script:

```
discord_clash_bot/
├── api/     external Clash of Clans API client
├── cogs/    Discord command groups
├── db/      persistence
├── cli/     command-line entry points
└── utils/   shared helpers
```

Layers are separated so the API client can be tested without a Discord connection, and the
command handlers without a live API. CI runs unit tests, coverage and Pylint on every push.

## Setup

```bash
pip install -r requirements.txt
cp secrets.toml.template secrets.toml   # add your Discord and Clash of Clans tokens
python -m discord_clash_bot.main
```

`secrets.toml` is gitignored — the template documents which keys are needed without
committing any of them.

---

Built by **[Christopher Manzano Vimos](https://manapple.dev)** — Data Scientist & AI Engineer.
The production work is at [manapple.dev](https://manapple.dev); this one is for fun.
