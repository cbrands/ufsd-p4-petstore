#!/usr/bin/env python3
'''
This script populates the database with some data.
4 categories are added and populated with pets.
the fish category is left empty to show that the
application can handle an empty category.
'''


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Pet, Category


def addCategory(category):
    '''
    This function adds a category
    '''
    myCategory = Category(name=category)
    session.add(myCategory)
    session.commit()
    return myCategory


def addPet(category, pet):
    '''
    This function adds a pet to a category
    '''
    pet.category_id = category.id
    session.add(pet)
    session.commit()

# Connect to database and start a session
engine = create_engine('sqlite:///petstore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# add categories
catCategory = addCategory("Cats")
dogCategory = addCategory("Dogs")
birdCategory = addCategory("Birds")
fishCategory = addCategory("Fish")

# Add pets
addPet(catCategory,
       Pet(name="Buster",
           description="I thought I saw a pussycat!",
           image_source="http://www.lolcats.com/images/u/07/42/lolcatsdotcomzj8wl73l6cxs1vvm.jpg"))  # noqa
addPet(catCategory,
       Pet(name="Ninja",
           description="Ninja is a sweet kitten, a delightful companion for your other pets.",  # noqa
           image_source="http://www.lolcats.com/images/u/07/32/lolcatsdotcomfbw0wlk98asucaok.jpg"))  # noqa
addPet(catCategory,
       Pet(name="Smiley",
           description="Smiley is as lovable as a cat can be.",
           image_source="http://www.lolcats.com/images/u/08/39/lolcatsdotcomly2r5yakozqlbhmn.jpg"))  # noqa
addPet(dogCategory,
       Pet(name="Sunshine",
           description="Sunshine is a dog that is always happy.",
           image_source="https://i.chzbgr.com/full/9059101440/h61CB217F/"))
addPet(dogCategory,
       Pet(name="Pug",
           description="Pug is a dog following the latest trends",
           image_source="https://i.chzbgr.com/full/9057932288/h38F9EC5E/"))
addPet(birdCategory,
       Pet(name="Fuzzy",
           description="Fuzzy is a friendly bird",
           image_source="https://i.chzbgr.com/full/2527119872/h3D84C38C/"))
