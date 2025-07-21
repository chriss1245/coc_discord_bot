from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Clan(Base):
    """
    Clan of clash of clans
    """

    __tablename__ = "clan"
    tag = Column(String, primary_key=True)
    name = Column(String)
    members = relationship("Member", backref="clan")

    def __init__(self, tag, name):
        self.tag = tag
        self.name = name


class Player(Base):
    """
    Clash of clans member table
    """

    __tablename__ = "member"
    name = Column(String)
    tag = Column(String, primary_key=True)
    clan_tag = Column(String, ForeignKey("clan.tag"))
    role = Column(String)
    war_preference = Column(String, nullable=True)

    def __init__(self, name, tag, clan_tag, role, war_preference=None):
        self.name = name
        self.tag = tag
        self.clan_tag = clan_tag
        self.role = role.replace("admin", "elder")
        self.war_preference = war_preference


class Spell(Base):
    """
    Table with the levels of spells of the members
    """

    __tablename__ = "spell"
    id = Column(Integer, primary_key=True)
    member_tag = Column(Integer, ForeignKey("member.tag"))
    spell = Column(String)
    level = Column(Integer)
    village = Column(String)

    def __init__(self, member_tag, spell, level, village):
        self.member_tag = member_tag
        self.spell = spell
        self.level = level
        self.village = village


class Heroe(Base):
    """
    Table with the levels of heros of the members
    """

    __tablename__ = "hero"
    id = Column(Integer, primary_key=True)
    member_tag = Column(Integer, ForeignKey("member.tag"))
    hero = Column(String)
    level = Column(Integer)
    village = Column(String)

    def __init__(self, member_tag, hero, level, village):
        self.member_tag = member_tag
        self.hero = hero
        self.level = level
        self.village = village


class Troop(Base):
    """
    Table with the levels of troops of the members
    """

    __tablename__ = "troop"
    id = Column(Integer, primary_key=True)
    member_tag = Column(Integer, ForeignKey("member.tag"))
    troop = Column(String)
    level = Column(Integer)
    village = Column(String)

    def __init__(self, member_tag, troop, level, village):
        self.member_tag = member_tag
        self.troop = troop
        self.level = level
        self.village = village


class War(Base):
    """
    Table with the wars of the clan
    """

    __tablename__ = "war"
    id = Column(Integer, primary_key=True)
    opponent = Column(String)
    result = Column(String)
    stars = Column(Integer)
    destruction = Column(Integer)

    def __init__(self, clan_tag, opponent, result, stars, destruction):
        self.clan_tag = clan_tag
        self.opponent = opponent
        self.result = result
        self.stars = stars
        self.destruction = destruction
