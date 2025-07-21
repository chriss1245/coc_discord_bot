"""
Test admin cog functionality.
"""

import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio
from discord import Member, User, Guild
from discord.ext.commands import Context

from discord_clash_bot.cogs.admin import AdminCog


class TestAdminCog(unittest.TestCase):
    """Test admin cog functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_bot = MagicMock()
        self.mock_bot.owner_ids = [12345]  # Mock bot owner ID
        self.admin_cog = AdminCog(self.mock_bot)

    def test_admin_cog_initialization(self):
        """Test that AdminCog initializes correctly."""
        self.assertEqual(self.admin_cog.bot, self.mock_bot)
        self.assertIsNotNone(self.admin_cog.coc_client)
        self.assertEqual(self.admin_cog.allowed_roles, ["admin"])

    def test_cog_check_with_admin_member(self):
        """Test cog_check returns True for member with admin role."""
        mock_ctx = MagicMock(spec=Context)
        mock_member = MagicMock(spec=Member)
        
        # Create mock role with admin name
        mock_role = MagicMock()
        mock_role.name = "admin"
        mock_member.roles = [mock_role]
        mock_ctx.author = mock_member
        
        result = self.admin_cog.cog_check(mock_ctx)
        self.assertTrue(result)

    def test_cog_check_with_non_admin_member(self):
        """Test cog_check returns False for member without admin role."""
        mock_ctx = MagicMock(spec=Context)
        mock_member = MagicMock(spec=Member)
        
        # Create mock role with non-admin name
        mock_role = MagicMock()
        mock_role.name = "member"
        mock_member.roles = [mock_role]
        mock_ctx.author = mock_member
        
        result = self.admin_cog.cog_check(mock_ctx)
        self.assertFalse(result)

    def test_cog_check_with_bot_owner_user(self):
        """Test cog_check returns True for bot owner (User, not Member)."""
        mock_ctx = MagicMock(spec=Context)
        mock_user = MagicMock(spec=User)
        mock_user.id = 12345  # Bot owner ID
        mock_ctx.author = mock_user
        
        result = self.admin_cog.cog_check(mock_ctx)
        self.assertTrue(result)

    def test_cog_check_with_non_owner_user(self):
        """Test cog_check returns False for non-owner User."""
        mock_ctx = MagicMock(spec=Context)
        mock_user = MagicMock(spec=User)
        mock_user.id = 99999  # Not bot owner ID
        mock_ctx.author = mock_user
        
        result = self.admin_cog.cog_check(mock_ctx)
        self.assertFalse(result)

    async def test_on_guild_join_event(self):
        """Test on_guild_join event handler."""
        # Mock guild and owner
        mock_guild = MagicMock(spec=Guild)
        mock_guild.name = "Test Guild"
        mock_owner = AsyncMock()
        mock_guild.owner = mock_owner
        
        # Call the event handler
        await self.admin_cog.on_guild_join(mock_guild)
        
        # Verify that a message was sent to the guild owner
        mock_owner.send.assert_called_once()
        sent_message = mock_owner.send.call_args[0][0]
        self.assertIn("Test Guild", sent_message)
        self.assertIn("!setup_discord", sent_message)

    async def test_setup_bot_command_with_member(self):
        """Test setup_bot command when called by a Member."""
        mock_ctx = AsyncMock(spec=Context)
        mock_member = MagicMock(spec=Member)
        mock_ctx.author = mock_member
        
        # Access the callback function directly
        setup_bot_command = getattr(self.admin_cog, 'setup_bot')
        if hasattr(setup_bot_command, 'callback'):
            await setup_bot_command.callback(self.admin_cog, mock_ctx)
        else:
            await setup_bot_command(mock_ctx)
        
        # Verify that a DM message was sent
        mock_ctx.send.assert_called_once()
        sent_message = mock_ctx.send.call_args[0][0]
        self.assertIn("DM", sent_message)

    async def test_setup_bot_command_with_user(self):
        """Test setup_bot command when called by a User (in DM)."""
        mock_ctx = AsyncMock(spec=Context)
        mock_user = MagicMock(spec=User)
        mock_ctx.author = mock_user
        
        # Access the callback function directly
        setup_bot_command = getattr(self.admin_cog, 'setup_bot')
        if hasattr(setup_bot_command, 'callback'):
            await setup_bot_command.callback(self.admin_cog, mock_ctx)
        else:
            await setup_bot_command(mock_ctx)
        
        # Verify no message was sent (not implemented for DM)
        mock_ctx.send.assert_not_called()

    async def test_cog_command_error_is_abstract(self):
        """Test that cog_command_error is now implemented."""
        mock_ctx = AsyncMock(spec=Context)
        mock_error = Exception("Test error")
        
        # Call the error handler
        await self.admin_cog.cog_command_error(mock_ctx, mock_error)
        
        # Verify that send was called with an error message
        mock_ctx.send.assert_called_once()
        sent_message = mock_ctx.send.call_args[0][0]
        self.assertIn("error occurred", sent_message)


def async_test(func):
    """Decorator to run async tests."""
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


# Apply the decorator to async test methods
TestAdminCog.test_on_guild_join_event = async_test(TestAdminCog.test_on_guild_join_event)
TestAdminCog.test_setup_bot_command_with_member = async_test(TestAdminCog.test_setup_bot_command_with_member)
TestAdminCog.test_setup_bot_command_with_user = async_test(TestAdminCog.test_setup_bot_command_with_user)
TestAdminCog.test_cog_command_error_is_abstract = async_test(TestAdminCog.test_cog_command_error_is_abstract)


if __name__ == "__main__":
    unittest.main()