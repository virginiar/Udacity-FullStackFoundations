import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Restaurant Class
class Restaurant(Base):

    __tablename__ = 'restaurant'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)

    @property
    def serialize(self):
        """
        Return object data in easily serializable format
        """
        return {
            'name': self.name,
            'id' : self.id,
        }

# Menu Item Class
class MenuItem(Base):

    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    course = Column(String(80))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        """
        Return object data in a easily serializable format
        """
        return {
        'name' : self.name,
        'description' : self.description,
        'id' : self.id,
        'price' : self.price,
        'course' : self.course,
        }

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)