"""
Module Docstring
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    """
    Class Docstring here.
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    @property
    def serialize(self):
        """
        Return object data in easily serializeable format
        """
        return {
            'id': self.id,
            'name': self.name,
        }

class Item(Base):
    """
    Class Docstring here.
    """
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    @property
    def serialize(self):
        """
        Return object data in easily serializeable format
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
        }

engine = create_engine('sqlite:///itemCatalog.db')
 

Base.metadata.create_all(engine)
    
