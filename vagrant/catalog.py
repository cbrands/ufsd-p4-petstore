#!/usr/bin/env python3

from flask import Flask, render_template, jsonify
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
    return render_template("index.html", categories=categories, pets=pets, selectedCategoryName="None")

@app.route('/login')
def login():
    return "loginpage"

@app.route('/catalog/<string:category_name>/')
def showCategory(category_name):
    categories = session.query(Category).all()
    selectedCategory = session.query(Category).filter_by(name=category_name).one()
    pets = session.query(Pet).filter_by(category_id=selectedCategory.id)
    return render_template("index.html", categories=categories, pets=pets, selectedCategoryName=selectedCategory.name)

@app.route('/catalog/<string:category_name>/<int:pet_id>/')
def showPet(category_name, pet_id):
    selectedPet = session.query(Pet).filter_by(id=pet_id).one()
    return render_template("item.html", category_name=category_name, selectedPet=selectedPet)

@app.route('/catalog/<string:category_name>/new/')
def newMenuItem(category_name):
    return "page to create a new pet"


@app.route('/catalog/<string:category_name>/<int:pet_id>/edit/')
def editMenuItem(category_name, pet_id):
    return "page to edit a pet"

@app.route('/catalog/<string:category_name>/<int:pet_id>/delete/')
def deleteMenuItem(category_name, pet_id):
    return "page to delete a pet"

@app.route('/catalog/JSON')
def showAllJSON():
    categories = session.query(Category).all()
    pets = session.query(Pet).all()
    return jsonify(categories=[c.serialize for c in categories], pets=[p.serialize for p in pets])

@app.route('/catalog/<string:category_name>/JSON')
def showCategoryJSON(category_name):
    categories = session.query(Category).all()
    selectedCategory = session.query(Category).filter_by(name=category_name).one()
    pets = session.query(Pet).filter_by(category_id=selectedCategory.id)
    return jsonify(categories=[c.serialize for c in categories], pets=[p.serialize for p in pets], selectedCategoryName=selectedCategory.name)

@app.route('/catalog/<string:category_name>/<int:pet_id>/JSON')
def showPetJSON(category_name, pet_id):
    selectedPet = session.query(Pet).filter_by(id=pet_id).one()
    return jsonify(selectedPet.serialize)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)