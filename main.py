# =======================================================================
# Project: Female Supervillain Trading Card App (template version)
# Description: An interactive web application built with Python.
# Built with: Flask and Flask-SQLAlchemy. The app's data is stored in an SQL database. Jinja places data in the app's HTML template.
# The app lets users:
# - add and delete female supervillain trading cards to/from a database.
# Background: Coursework for Skillcrush's "Using Python to Build Web Apps" course.

# ==== *** ====

# The main.py file contains the code that manages the logic of/operates the app. It:
# - creates the database model and manages interaction with the database.
# - contains routing for rendering the HTML templates, querying the database, adding new villains to the database, and for deleting existing villains from the database.
# - handles error communication.
# =======================================================================

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask("app")

#Configures database root location and connects project to SQLAlchemy toolkit:
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///villain.db"
db = SQLAlchemy(app)


#Creates database model and columns:
class Villain(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(250), nullable=False)
  interests = db.Column(db.String(205), nullable=False)
  url = db.Column(db.String(250), nullable=False)
  date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  #Specifies how to present the Villain object when called:
  def __repr__(self):
    return "<Villain " + self.name + ">"


#Creates database and commits changes:
with app.app_context():
  db.create_all()
  db.session.commit()


#Renders HTML for main villain page with all villains:
@app.route("/")
def villains_cards():
  return render_template("villain.html", villains=Villain.query.all())


#Renders HTML for page where user adds a new villain to the database and holds error messages if user fails to add all fields:
@app.route("/add", methods=["GET"])
def add_villain():
  return render_template("addvillain.html", errors=[])


#Renders HTML page where user deletes villain from database and holds error message:
@app.route("/delete", methods=["GET"])
def delete_villain():
  return render_template("deletevillain.html", errors=[])


#Adds new villain to database when user fills out HTML villain form:
@app.route("/addVillain", methods=["POST"])
def add_user():
  #Holds error messages to user if they fail to submit required form fields:
  errors = []
  #Checks if villain's information has been submitted on the HTML villain form and adds  message to errors list if any information is missing:
  name = request.form.get("name")
  if not name:
    errors.append("Oops! Looks like you forgot to add a name!")
  description = request.form.get("description")
  if not description:
    errors.append("Oops! Looks like you forgot to add a description!")
  interests = request.form.get("interests")
  if not interests:
    errors.append("Oops! Looks like you forgot to add interests!")
  url = request.form.get("url")
  if not url:
    errors.append("Oops! Looks like you forgot an image!")
  #Searches database to see if the villain the user is trying to add already exists and if so adds message to errors list:
  villain = Villain.query.filter_by(name=name).first()
  if villain:
    errors.append("Oops! A villain with that name already exists!")
  #Handles HTML template rendering when information on the form is missing and displays error message:
  if errors:
    return render_template("addvillain.html", errors=errors)
  #Adds new villain to database if no errors are found and renders HTML main page with all villains:
  else:
    new_villain = Villain(name=name,
                          description=description,
                          interests=interests,
                          url=url)
    db.session.add(new_villain)
    db.session.commit()
    return render_template("villain.html", villains=Villain.query.all())


#Removes existing villain from database:
@app.route("/deleteVillain", methods=["POST"])
def delete_user():
  #Gets villain name inputted on the HTML form:
  name = request.form.get("name")
  #Checks if inputted villain exists in the database and if so: 1) deletes villain, and 2) renders HTML main page with all villains minus deleted villain:
  villain = Villain.query.filter_by(name=name).first()
  if villain:
    db.session.delete(villain)
    db.session.commit()
    return render_template("villain.html", villains=Villain.query.all())
  #Renders the delete villain HTML page with error message if inputted villain does not exist in the database:
  else:
    return render_template("deletevillain.html",
                           errors=["Oops! That villain doesn't exist!"])


app.run(host='0.0.0.0', port=8080)
