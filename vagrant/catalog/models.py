"""Define ORM for the itemCatelog database.

Classes:
    Category: A Category represents a general grouping (category) that various items can belong to.
    Item: An Item represents a specific thing, that belongs to a larger group (Category) of things.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """User class for use with the sqlalchemy ORM.

    Keeps track of registered users' email and name in the system.

    Attributes:
        id: An integer representing the database id of Item object.
        name: A string containing the name of the registered user.
        email: A string containing the email of the registered user.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

class Category(Base):
    """Category class for use with the sqlalchemy ORM.

    A Category represents a general grouping (category) that various items can belong to.
    Each Item can only belong to one Category.
    Example:
        'Books' is a Category for the Items: 'The Forever War', 'The Foundation'.

    Attributes:
        id: An integer representing the database id of category object.
        name: A string representing the name assigned to the Category object.
        user_id: An integer representing the foriegn key of the associated User object.
        user: The User object associated to the Item object.
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return Category data in easily serializeable format

        Returns:
            Dictionary representaiton of Category object in a format that is easily serializable to JSON.
        """
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
        }

class Item(Base):
    """Item class for use with the sqlalchemy ORM.

    An Item represents a specific thing, that belongs to a larger group (Category) of things.
    Example:
         'The Forever War', 'Ender's Game', 'The Foundation' are Items with Category 'Books'.

    Attributes:
        id: An integer representing the database id of Item object.
        name: A string representing the name assigned to the Item object.
        description: A string representing the description assigned to the Item object.
        category_id: An integer representing the foriegn key of the associated Category object.
        category: The Category object associated with the Item object.
        user_id: An integer representing the foriegn key of the associated User object.
        user: The User object associated to the Item object.
    """
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return Item data in easily serializeable format

        Returns:
            Dictionary representaiton of Item object in a format that is easily serializable to JSON.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name,
            'user_id': self.user_id,
        }

engine = create_engine('sqlite:///itemCatalog.db')


Base.metadata.create_all(engine)

