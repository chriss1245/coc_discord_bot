"""
Tests of the base cog functionality
"""

import unittest
from unittest.mock import MagicMock, AsyncMock
from discord import Member, User
from discord.ext.commands import Context

from discord_clash_bot.cogs.base_cog import BaseCog, Role


class MockCog(BaseCog):
    """
    Mock cog for testing
    """

    def __init__(self, bot):
        self.bot = bot
        self.allowed_roles = ["admin", "member"]

    async def cog_command_error(self, ctx, error):
        """
        Handle errors
        Args:
            ctx: context
            error: error
        """
        pass

    def cog_check(self, ctx: Context) -> bool:
        """Test implementation of cog_check."""
        if isinstance(ctx.author, Member):
            return any(role.name in self.allowed_roles for role in ctx.author.roles)
        return False


class TestBaseCog(unittest.TestCase):
    """Test base cog functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_bot = MagicMock()
        self.mock_cog = MockCog(self.mock_bot)

    def test_role_enum_values(self):
        """Test that Role enum has all expected values."""
        expected_roles = ['admin', 'leader', 'coleader', 'elder', 'member', 'foreigner']
        for role in expected_roles:
            self.assertTrue(hasattr(Role, role.upper()))
            self.assertEqual(getattr(Role, role.upper()).value, role)

    def test_base_cog_initialization(self):
        """Test that BaseCog initializes correctly."""
        self.assertEqual(self.mock_cog.bot, self.mock_bot)

    def test_cog_check_with_member_allowed_role(self):
        """Test cog_check returns True for member with allowed role."""
        # Create mock context with member that has allowed role
        mock_ctx = MagicMock(spec=Context)
        mock_member = MagicMock(spec=Member)
        
        # Create mock role with allowed name
        mock_role = MagicMock()
        mock_role.name = "admin"
        mock_member.roles = [mock_role]
        mock_ctx.author = mock_member
        
        result = self.mock_cog.cog_check(mock_ctx)
        self.assertTrue(result)

    def test_cog_check_with_member_disallowed_role(self):
        """Test cog_check returns False for member with disallowed role."""
        mock_ctx = MagicMock(spec=Context)
        mock_member = MagicMock(spec=Member)
        
        # Create mock role with disallowed name
        mock_role = MagicMock()
        mock_role.name = "foreigner"
        mock_member.roles = [mock_role]
        mock_ctx.author = mock_member
        
        result = self.mock_cog.cog_check(mock_ctx)
        self.assertFalse(result)

    def test_cog_check_with_user_not_member(self):
        """Test cog_check returns False for User (not Member)."""
        mock_ctx = MagicMock(spec=Context)
        mock_user = MagicMock(spec=User)
        mock_ctx.author = mock_user
        
        result = self.mock_cog.cog_check(mock_ctx)
        self.assertFalse(result)

    def test_cog_check_with_member_multiple_roles(self):
        """Test cog_check with member having multiple roles."""
        mock_ctx = MagicMock(spec=Context)
        mock_member = MagicMock(spec=Member)
        
        # Create multiple roles, one allowed and one not
        mock_role1 = MagicMock()
        mock_role1.name = "foreigner"
        mock_role2 = MagicMock()
        mock_role2.name = "member"
        mock_member.roles = [mock_role1, mock_role2]
        mock_ctx.author = mock_member
        
        result = self.mock_cog.cog_check(mock_ctx)
        self.assertTrue(result)

    async def test_ping_command_exists(self):
        """Test that ping command exists and is callable."""
        # Mock context for ping command
        mock_ctx = AsyncMock(spec=Context)
        
        # Access the callback function directly (bypass the command decorator)
        ping_command = getattr(self.mock_cog, 'ping')
        if hasattr(ping_command, 'callback'):
            # This is a command object, get the actual function
            await ping_command.callback(self.mock_cog, mock_ctx)
        else:
            # Direct function call
            await ping_command(mock_ctx)
        
        # Verify send was called with correct message
        mock_ctx.send.assert_called_once_with("pong")


def async_test(func):
    """Decorator to run async tests."""
    import asyncio
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


# Apply the decorator to async test methods
TestBaseCog.test_ping_command_exists = async_test(TestBaseCog.test_ping_command_exists)


if __name__ == "__main__":
    unittest.main()
