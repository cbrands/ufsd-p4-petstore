#!/usr/bin/env python3

from flask import Flask, render_template, jsonify, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Pet, Category
# imports needed for security
from flask import session as login_session
import random
import string
# imports needed for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Petstore1"

engine = create_engine('sqlite:///petstore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    '''
    Create anti-forgery state token
    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''
    This function is adapted from Udacity fullstack nanodegree
    lesson 11 Creating Google sign in
    here we use google to login
    '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    preJson = h.request(url, 'GET')[1]
    result = json.loads(preJson.decode("utf-8"))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;'
    output += 'border-radius: 150px;-webkit-border-radius: 150px;'
    output += '-moz-border-radius: 150px;"> '
    print("logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    '''
    This function is adapted from Udacity fullstack nanodegree
    lesson 11 Creating Google sign in
    here we disconnect
    '''
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print(response)
        return redirect(url_for('showAll'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        print(response)
        return redirect(url_for('showAll'))


@app.route('/')
@app.route('/catalog/')
def showAll():
    '''
    Mainpage. query for all categories and all pets and show them
    on index.html.
    '''
    if 'username' not in login_session:
        showLoginButton = True
    else:
        showLoginButton = False
    categories = session.query(Category).all()
    pets = session.query(Pet).all()
    return render_template("index.html",
                           categories=categories, pets=pets,
                           selectedCategoryName="None",
                           showLoginButton=showLoginButton)


@app.route('/catalog/<string:category_name>/')
def showCategory(category_name):
    '''
    Categorypage. query for all categories (for the side bar) and the
    pets belonging to the selected category and show them on index.html.
    '''
    if 'username' not in login_session:
        showLoginButton = True
    else:
        showLoginButton = False
    categories = session.query(Category).all()
    selectedCategory = session.query(Category).filter_by(
        name=category_name).one()
    pets = session.query(Pet).filter_by(category_id=selectedCategory.id)
    return render_template("index.html",
                           categories=categories, pets=pets,
                           selectedCategoryName=selectedCategory.name,
                           showLoginButton=showLoginButton)


@app.route('/catalog/<string:category_name>/<int:pet_id>/')
def showPet(category_name, pet_id):
    '''
    Show the selected pet
    '''
    if 'username' not in login_session:
        showLoginButton = True
    else:
        showLoginButton = False
    selectedPet = session.query(Pet).filter_by(id=pet_id).one()
    return render_template("item.html",
                           selectedCategoryName=category_name,
                           selectedPet=selectedPet,
                           showLoginButton=showLoginButton)


@app.route('/catalog/<string:category_name>/new/', methods=['GET', 'POST'])
def newPet(category_name):
    '''
    Create a new pet if the user is logged in otherwise redirect
    to login page.
    If this method is called with a GET request then new.html is shown
    If this method is called with a post request the new pet is saved
    '''
    if 'username' not in login_session:
        return redirect('/login')
    selectedCategory = session.query(Category).filter_by(
        name=category_name).one()
    if request.method == 'POST':
        newPet = Pet(
            name=request.form['name'],
            description=request.form['description'],
            image_source=request.form['source'],
            category_id=selectedCategory.id)
        session.add(newPet)
        session.commit()
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('new.html', selectedCategory=selectedCategory)


@app.route('/catalog/<string:category_name>/<int:pet_id>/edit/',
           methods=['GET', 'POST'])
def editPet(category_name, pet_id):
    '''
    Edit pet if the user is logged in otherwise redirect
    to login page.
    If this method is called with a GET request then edit.html is shown
    If this method is called with a post request the pet is saved
    '''
    if 'username' not in login_session:
        return redirect('/login')
    selectedCategory = session.query(Category).filter_by(
        name=category_name).one()
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
        return render_template('edit.html',
                               selectedCategory=selectedCategory,
                               selectedPet=selectedPet)


@app.route('/catalog/<string:category_name>/<int:pet_id>/delete/',
           methods=['GET', 'POST'])
def deletePet(category_name, pet_id):
    '''
    Delete pet if the user is logged in otherwise redirect
    to login page.
    If this method is called with a GET request then delete.html is shown
    If this method is called with a post request the pet is deleted
    '''
    if 'username' not in login_session:
        return redirect('/login')
    selectedCategory = session.query(Category).filter_by(
        name=category_name).one()
    selectedPet = session.query(Pet).filter_by(id=pet_id).one()
    if request.method == 'POST':
        session.delete(selectedPet)
        session.commit()
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('delete.html',
                               selectedCategory=selectedCategory,
                               selectedPet=selectedPet)


@app.route('/catalog/JSON')
def showAllJSON():
    '''
    Shows JSON data from all pets and categories
    '''
    categories = session.query(Category).all()
    pets = session.query(Pet).all()
    return jsonify(categories=[c.serialize for c in categories],
                   pets=[p.serialize for p in pets])


@app.route('/catalog/<string:category_name>/JSON')
def showCategoryJSON(category_name):
    '''
    Shows JSON data from all pets belonging to the selected category
    '''
    categories = session.query(Category).all()
    selectedCategory = session.query(Category).filter_by(
        name=category_name).one()
    pets = session.query(Pet).filter_by(category_id=selectedCategory.id)
    return jsonify(categories=[c.serialize for c in categories],
                   pets=[p.serialize for p in pets],
                   selectedCategoryName=selectedCategory.name)


@app.route('/catalog/<string:category_name>/<int:pet_id>/JSON')
def showPetJSON(category_name, pet_id):
    '''
    Shows JSON data from the selected pet
    '''
    selectedPet = session.query(Pet).filter_by(id=pet_id).one()
    return jsonify(selectedPet.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
