"""
Test database schema models.
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from discord_clash_bot.db.schema import (
    Base, Clan, Player, Spell, Heroe, Troop, War
)


class TestDatabaseSchema(unittest.TestCase):
    """Test database schema functionality."""

    def setUp(self):
        """Set up test database."""
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        """Clean up test database."""
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_clan_creation(self):
        """Test clan model creation."""
        clan = Clan(tag="#TEST123", name="Test Clan")
        self.assertEqual(clan.tag, "#TEST123")
        self.assertEqual(clan.name, "Test Clan")

    def test_player_creation(self):
        """Test player model creation."""
        player = Player(
            name="Test Player",
            tag="#PLAYER123",
            clan_tag="#TEST123",
            role="member"
        )
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(player.tag, "#PLAYER123")
        self.assertEqual(player.clan_tag, "#TEST123")
        self.assertEqual(player.role, "member")

    def test_player_admin_role_conversion(self):
        """Test that admin role is converted to elder."""
        player = Player(
            name="Test Admin",
            tag="#ADMIN123",
            clan_tag="#TEST123",
            role="admin"
        )
        self.assertEqual(player.role, "elder")

    def test_player_with_war_preference(self):
        """Test player creation with war preference."""
        player = Player(
            name="Test Player",
            tag="#PLAYER123",
            clan_tag="#TEST123",
            role="member",
            war_preference="in"
        )
        self.assertEqual(player.war_preference, "in")

    def test_spell_creation(self):
        """Test spell model creation."""
        spell = Spell(
            member_tag="#PLAYER123",
            spell="Lightning",
            level=7,
            village="home"
        )
        self.assertEqual(spell.member_tag, "#PLAYER123")
        self.assertEqual(spell.spell, "Lightning")
        self.assertEqual(spell.level, 7)
        self.assertEqual(spell.village, "home")

    def test_heroe_creation(self):
        """Test hero model creation."""
        hero = Heroe(
            member_tag="#PLAYER123",
            hero="Barbarian King",
            level=65,
            village="home"
        )
        self.assertEqual(hero.member_tag, "#PLAYER123")
        self.assertEqual(hero.hero, "Barbarian King")
        self.assertEqual(hero.level, 65)
        self.assertEqual(hero.village, "home")

    def test_troop_creation(self):
        """Test troop model creation."""
        troop = Troop(
            member_tag="#PLAYER123",
            troop="Dragon",
            level=8,
            village="home"
        )
        self.assertEqual(troop.member_tag, "#PLAYER123")
        self.assertEqual(troop.troop, "Dragon")
        self.assertEqual(troop.level, 8)
        self.assertEqual(troop.village, "home")

    def test_war_creation(self):
        """Test war model creation."""
        war = War(
            clan_tag="#TEST123",
            opponent="Enemy Clan",
            result="victory",
            stars=45,
            destruction=95
        )
        self.assertEqual(war.clan_tag, "#TEST123")
        self.assertEqual(war.opponent, "Enemy Clan")
        self.assertEqual(war.result, "victory")
        self.assertEqual(war.stars, 45)
        self.assertEqual(war.destruction, 95)

    def test_database_relationships(self):
        """Test database relationships between models."""
        # Create and add a clan
        clan = Clan(tag="#TEST123", name="Test Clan")
        self.session.add(clan)

        # Create and add a player
        player = Player(
            name="Test Player",
            tag="#PLAYER123",
            clan_tag="#TEST123",
            role="member"
        )
        self.session.add(player)
        self.session.commit()

        # Test relationship
        db_clan = self.session.query(Clan).filter_by(tag="#TEST123").first()
        self.assertIsNotNone(db_clan)
        self.assertEqual(len(db_clan.members), 1)
        self.assertEqual(db_clan.members[0].name, "Test Player")


if __name__ == "__main__":
    unittest.main()