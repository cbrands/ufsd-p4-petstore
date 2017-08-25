#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/catalog')
def showAll():
    return "mainpage"

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