"""
Install the package
"""

from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().split("\n")

setup(
    name="discord_clash_bot",
    version="23.05.28",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": ["discord_clash_bot = discord_clash_bot.cli.commands:cli"]
    },
)
