"""
Database connection, creation, and management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .schema import Base

class DBConnection():
    """
    Database connection class
    """

    def __init__(self, db_url="sqlite:///clash.db"):
        self.engine = create_engine(db_url)
        self.session = sessionmaker(bind=self.engine)()

    def create_all(self):
        """
        Create all tables
        """
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        """
        Drop all tables
        """
        Base.metadata.drop_all(self.engine)

    def add(self, obj):
        """
        Add an object to the session
        """
        if isinstance(obj, list):
            self.session.add_all(obj)
        else:
            self.session.add(obj)
        self.session.commit()
