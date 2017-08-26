#!/usr/bin/env python3

from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Pet, User, Category

# imports needed for security
from flask import session as login_session
import random
import string


engine = create_engine('sqlite:///petstore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return "The current session state is %s" % login_session['state']


@app.route('/')
@app.route('/catalog/')
def showAll():
    categories = session.query(Category).all()
    pets = session.query(Pet).all()
    return render_template("index.html", categories=categories, pets=pets, selectedCategoryName="None")


@app.route('/catalog/<string:category_name>/')
def showCategory(category_name):
    categories = session.query(Category).all()
    selectedCategory = session.query(Category).filter_by(name=category_name).one()
    pets = session.query(Pet).filter_by(category_id=selectedCategory.id)
    return render_template("index.html", categories=categories, pets=pets, selectedCategoryName=selectedCategory.name)

@app.route('/catalog/<string:category_name>/<int:pet_id>/')
def showPet(category_name, pet_id):
    selectedPet = session.query(Pet).filter_by(id=pet_id).one()
    return render_template("item.html", selectedCategoryName=category_name, selectedPet=selectedPet)

@app.route('/catalog/<string:category_name>/new/', methods=['GET', 'POST'])
def newPet(category_name):
    selectedCategory = session.query(Category).filter_by(name=category_name).one()
    if request.method == 'POST':
        newPet = Pet(
            name=request.form['name'], description=request.form['description'], image_source=request.form['source'], category_id=selectedCategory.id)
        session.add(newPet)
        session.commit()
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('new.html', selectedCategory=selectedCategory)


@app.route('/catalog/<string:category_name>/<int:pet_id>/edit/', methods=['GET', 'POST'])
def editPet(category_name, pet_id):
    selectedCategory = session.query(Category).filter_by(name=category_name).one()
    selectedPet = session.query(Pet).filter_by(id=pet_id).one()
    if request.method == 'POST':
        if request.form['name']:
            selectedPet.name = request.form['name']
        if request.form['description']:
            selectedPet.description = request.form['description']
        if request.form['source']:
            selectedPet.image_source = request.form['source']
        session.add(selectedPet)
        session.commit()
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('edit.html', selectedCategory=selectedCategory, selectedPet=selectedPet)

@app.route('/catalog/<string:category_name>/<int:pet_id>/delete/', methods=['GET', 'POST'])
def deletePet(category_name, pet_id):
    selectedCategory = session.query(Category).filter_by(name=category_name).one()
    selectedPet = session.query(Pet).filter_by(id=pet_id).one()
    if request.method == 'POST':
        session.delete(selectedPet)
        session.commit()
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('delete.html', selectedCategory=selectedCategory, selectedPet=selectedPet)

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
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)