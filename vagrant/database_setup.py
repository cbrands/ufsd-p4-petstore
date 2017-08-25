'''
This script sets up the database. It is adapted from 
Lesson 6 Working with CRUD
'''

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Pet(Base):
    __tablename__ = 'pet'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    image_source = Column(String(80))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_source': self.image_source,
            'category_id': self.category_id
        }


class User(Base):
    __tablename__ = 'user'
    
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    password = Column(String(80))


engine = create_engine('sqlite:///petstore.db')
Base.metadata.create_all(engine)