# ufsd-p4-petstore
## Introduction
This project is my implementation of the item\_catalog project. This is the fourth project of the Udacity Full stack developer nanodegree program.


## What you get.
* README.md (this file)
* .gitignore -- a file to make sure that not the whole virtual machine gets stored in git, you can ignore this file
* vagrant/.gitignore -- same as above
* vagrant/client\_secrets.json -- this file contans the secret code used by google for authentication
* vagrant/database\_setup.py -- This script creates the database and makes the necessary tables.
* vagrant/populate\_database.py -- This script loads testdata in the database
* vagrant/catalog.py -- this script is the actual application
* vagrant/static/style.css -- Simple ccs file, I did't want the app to be to ugly
* vagrant/templates/\*.html -- These are templates used by catalog.py to create the webpages

## How to start.
### Prerequisites
* [Virtualbox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)

### Preparing the environment
* [Download the virtual machine](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)
* unzip this file in a directory of your choice. This directory I will call $BASEDIR. Please replace $BASEDIR with your directory in the rest of these instructions.
* Open your terminal and type
```
cd $BASEDIR/vagrant
```
### Starting the application
To start the virtual machine and login type the following commands
```
vagrant up
vagrant ssh
```
Go to the /vagrant directory.
```
cd /vagrant
```
Create a database and populate the database with testdata
```
python3 database_setup.py
python3 populate_database.py
```
Start the program with
```
python3 catalog.py
```
You can now start the webrowser and open the page on localhost:5000

## Using the application

## Stopping
To logout and stop the virtual machine type
```
exit
vagrant halt
```