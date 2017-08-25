#!/usr/bin/env python3

from flask import Flask, render_template
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Pet, User, Category

engine = create_engine('sqlite:///petstore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/catalog')
def showAll():
    categories = session.query(Category).all()
    pets = session.query(Pet).all()
    return render_template("index.html", categories=categories, pets=pets)

@app.route('/login')
def login():
    return "loginpage"

@app.route('/catalog/<int:catagory_id>/')
def showCategory(catagory_id):
    return "categorypage"

@app.route('/catalog/<int:catagory_id>/new/')
def newMenuItem(catagory_id):
    return "page to create a new pet"


@app.route('/catalog/<int:catagory_id>/<int:pet_id>/edit/')
def editMenuItem(catagory_id, pet_id):
    return "page to edit a pet"



@app.route('/catalog/<int:catagory_id>/<int:pet_id>/delete/')
def deleteMenuItem(catagory_id, pet_id):
    return "page to delete a pet"


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)