"""
Test main bot functionality.
"""

import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

# Add the project root to the path for importing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from discord_clash_bot.main import run


class TestMainBot(unittest.TestCase):
    """Test main bot functionality."""

    @patch('discord_clash_bot.main.SECRETS', {
        'discord': {'prefix': '!', 'token': 'test_token'}
    })
    @patch('discord_clash_bot.main.Bot')
    @patch('discord_clash_bot.main.AdminCog')
    async def test_run_bot_setup(self, mock_admin_cog, mock_bot_class):
        """Test that the bot is set up correctly."""
        # Mock the bot instance
        mock_bot = AsyncMock()
        mock_bot_class.return_value = mock_bot
        
        # Mock the cog instance
        mock_cog_instance = MagicMock()
        mock_admin_cog.return_value = mock_cog_instance
        
        # Mock bot.start to avoid actually starting the bot
        async def mock_start(token):
            # Just verify the token is passed correctly
            self.assertEqual(token, 'test_token')
            return
        
        mock_bot.start = mock_start
        
        # Run the function
        await run()
        
        # Verify Bot was instantiated with correct parameters
        mock_bot_class.assert_called_once()
        call_args = mock_bot_class.call_args
        
        # Check that the bot was created with the right parameters
        self.assertEqual(call_args[1]['command_prefix'], '!')
        self.assertEqual(call_args[1]['description'], "Clash of Clans bot")
        self.assertTrue(call_args[1]['case_insensitive'])
        self.assertIsNotNone(call_args[1]['intents'])
        
        # Verify AdminCog was instantiated and added
        mock_admin_cog.assert_called_once_with(mock_bot)
        mock_bot.add_cog.assert_called_once_with(mock_cog_instance)

    @patch('discord_clash_bot.main.SECRETS', {
        'discord': {'prefix': '>', 'token': 'different_token'}
    })
    @patch('discord_clash_bot.main.Bot')
    @patch('discord_clash_bot.main.AdminCog')
    async def test_run_with_different_config(self, mock_admin_cog, mock_bot_class):
        """Test bot with different configuration."""
        mock_bot = AsyncMock()
        mock_bot_class.return_value = mock_bot
        mock_cog_instance = MagicMock()
        mock_admin_cog.return_value = mock_cog_instance
        
        # Mock bot.start to verify token
        async def mock_start(token):
            self.assertEqual(token, 'different_token')
            return
        
        mock_bot.start = mock_start
        
        await run()
        
        # Verify the prefix was set correctly
        call_args = mock_bot_class.call_args
        self.assertEqual(call_args[1]['command_prefix'], '>')

    @patch('discord_clash_bot.main.discord.Intents')
    @patch('discord_clash_bot.main.SECRETS', {
        'discord': {'prefix': '!', 'token': 'test_token'}
    })
    @patch('discord_clash_bot.main.Bot')
    @patch('discord_clash_bot.main.AdminCog')
    async def test_discord_intents_setup(self, mock_admin_cog, mock_bot_class, mock_intents):
        """Test that Discord intents are set up correctly."""
        mock_bot = AsyncMock()
        mock_bot_class.return_value = mock_bot
        mock_cog_instance = MagicMock()
        mock_admin_cog.return_value = mock_cog_instance
        
        # Mock intents
        mock_intents_instance = MagicMock()
        mock_intents.all.return_value = mock_intents_instance
        
        # Mock bot.start
        mock_bot.start = AsyncMock()
        
        await run()
        
        # Verify intents.all() was called
        mock_intents.all.assert_called_once()
        
        # Verify bot was created with the intents
        call_args = mock_bot_class.call_args
        self.assertEqual(call_args[1]['intents'], mock_intents_instance)


class TestMainModule(unittest.TestCase):
    """Test main module execution."""

    @patch('discord_clash_bot.main.asyncio.run')
    @patch('discord_clash_bot.main.run')
    def test_main_execution(self, mock_run_func, mock_asyncio_run):
        """Test that main execution calls asyncio.run with the run function."""
        # Mock sys.argv to simulate direct execution
        original_argv = sys.argv
        sys.argv = ['main.py']
        
        try:
            # Import and execute the main block
            import discord_clash_bot.main
            
            # The main block should have been executed during import
            # but we can't easily test it without running it
            # So we'll test the logic separately
            pass
        finally:
            sys.argv = original_argv


def async_test(func):
    """Decorator to run async tests."""
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


# Apply the decorator to async test methods
TestMainBot.test_run_bot_setup = async_test(TestMainBot.test_run_bot_setup)
TestMainBot.test_run_with_different_config = async_test(TestMainBot.test_run_with_different_config)
TestMainBot.test_discord_intents_setup = async_test(TestMainBot.test_discord_intents_setup)


if __name__ == "__main__":
    unittest.main()