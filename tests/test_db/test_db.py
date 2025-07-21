"""
Test database connection and management.
"""

import unittest
import tempfile
import os

from discord_clash_bot.db.db import DBConnection
from discord_clash_bot.db.schema import Clan, Player


class TestDBConnection(unittest.TestCase):
    """Test database connection functionality."""

    def setUp(self):
        """Set up test database with temporary file."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.db_url = f"sqlite:///{self.temp_db.name}"
        self.db = DBConnection(self.db_url)

    def tearDown(self):
        """Clean up temporary database file."""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_db_connection_init(self):
        """Test database connection initialization."""
        self.assertIsNotNone(self.db.engine)
        self.assertIsNotNone(self.db.session)

    def test_db_connection_default_url(self):
        """Test database connection with default URL."""
        default_db = DBConnection()
        self.assertIsNotNone(default_db.engine)
        self.assertIsNotNone(default_db.session)

    def test_create_all_tables(self):
        """Test creating all database tables."""
        self.db.create_all()
        # Test that tables exist by trying to query them
        from sqlalchemy import text
        result = self.db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        table_names = [row[0] for row in result.fetchall()]
        
        expected_tables = ['clan', 'member', 'spell', 'hero', 'troop', 'war']
        for table in expected_tables:
            self.assertIn(table, table_names)

    def test_drop_all_tables(self):
        """Test dropping all database tables."""
        self.db.create_all()
        self.db.drop_all()
        
        # Test that no tables exist
        from sqlalchemy import text
        result = self.db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        table_names = [row[0] for row in result.fetchall()]
        
        expected_tables = ['clan', 'member', 'spell', 'hero', 'troop', 'war']
        for table in expected_tables:
            self.assertNotIn(table, table_names)

    def test_add_single_object(self):
        """Test adding a single object to the database."""
        self.db.create_all()
        
        clan = Clan(tag="#TEST123", name="Test Clan")
        self.db.add(clan)
        
        # Verify the object was added
        result = self.db.session.query(Clan).filter_by(tag="#TEST123").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Test Clan")

    def test_add_list_of_objects(self):
        """Test adding a list of objects to the database."""
        self.db.create_all()
        
        objects = [
            Clan(tag="#CLAN1", name="Clan 1"),
            Clan(tag="#CLAN2", name="Clan 2"),
            Player(name="Player 1", tag="#PLAYER1", clan_tag="#CLAN1", role="member"),
            Player(name="Player 2", tag="#PLAYER2", clan_tag="#CLAN2", role="elder")
        ]
        
        self.db.add(objects)
        
        # Verify all objects were added
        clans = self.db.session.query(Clan).all()
        players = self.db.session.query(Player).all()
        
        self.assertEqual(len(clans), 2)
        self.assertEqual(len(players), 2)
        
        clan_tags = [clan.tag for clan in clans]
        self.assertIn("#CLAN1", clan_tags)
        self.assertIn("#CLAN2", clan_tags)


if __name__ == "__main__":
    unittest.main()