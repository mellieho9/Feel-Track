#imports

from functools import wraps
import os 

# flask imports 

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

# DB import
import psycopg2
import psycopg2.extras

# ML imports

import model
import pickle

# helper functions
from helpers import login_required


# Configure application
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# configure
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.testing = False
app.config["SESSION_PERMANENT"] = True


# Set up heroku database

DATABASE_URI = os.environ['DATABASE_URL']

# defining pages

@app.route("/", methods=["GET", "POST"])
def index():
    """Show Homepage"""
    if request.method == "POST":
        query = request.form.get("query")
        return redirect(f"/search/{query}")
    else:
        return render_template("index.html")

@app.route("/search/<query>")
def search(query):
    return render_template("search.html", query=query)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # connect to DB
        conn = psycopg2.connect(DATABASE_URI)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("SELECT * FROM users WHERE email = '%s'" % (request.form.get("email")))

        rows = cur.fetchall()

        if len(rows) == 1:
            if rows[0]["password"] == request.form.get("password"):
                # Remember which user has logged in
                session["user_id"] = rows[0]["id"]

                session["firstname"] = rows[0]["firstname"]

                session["lastname"] = rows[0]["lastname"]

                session["email"] = rows[0]["email"]

                session["phone"] = rows[0]["phone"]

                session["birthday"] = rows[0]["birthday"]

                return redirect("/emotional_survey")
            else:
                return apology("Incorrect credentials")
        else:
            return apology("Username doesn't exist")

        # log user in

        session.clear()
    
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        

        session.clear()

        # Register user
        conn = psycopg2.connect(DATABASE_URI)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Ensure email doesn 't exist

        cur.execute("SELECT * FROM users WHERE email = '%s'" % (request.form.get("email")))

        emails = cur.fetchall()

        print(len(emails))

        if len(emails) > 0:
            return apology("An account with that email already exists")

        # Ensure phone doesn 't exist

        cur.execute("SELECT * FROM users WHERE phone = '%s'" % (request.form.get("phone")))

        phones = cur.fetchall()

        if len(phones) > 0:
            return apology("An account with that phone number already exists")

        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        birthday = request.form.get("birthday")
        phone = request.form.get("phone")
        password = request.form.get("password")
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = """INSERT INTO users (firstname, lastname, email, birthday, phone, password) VALUES (%s,%s,%s,%s,%s,%s)"""
        info = (firstname, lastname, email, birthday, phone, password)
        
        # add user into database

        register_user = cur.execute(query, info)

        conn.commit()

        return redirect("/login")
    else:
        return render_template("signup.html")

@app.route("/emotional_survey", methods=["GET", "POST"])
def emotional_survey(): 
    if request.method == "POST":
        print(request.form.get("lv1"), request.form.get("lv5"))
        if request.form.get('lv1') != None or request.form.get('lv2') != None:
            return redirect("/health_survey")
        else:
            return redirect("/travel_inquiry")
    else:
        return render_template("emotional_survey.html")

@app.route("/health_survey", methods=["GET", "POST"])
@login_required
def health_survey():
  if request.method == "POST":

    symptoms = request.form.get("symptoms")

    illness = model.predictDisease(symptoms)

    if illness == None:
        return redirect(f"/self_diagnose")

    # add user's illness to database

    query = """UPDATE users SET illness = ('%s') WHERE id = (%s)"""
    info = (illness, session.get("user_id"))
    
    conn = psycopg2.connect(DATABASE_URI)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    add_illness = cur.execute(query % info)

    conn.commit()

    return redirect(f"/survey_results/{illness}")

  else:
    return render_template("health_survey.html")

@app.route("/survey_results/<illness>")
def survey_results(illness):
    return render_template("survey_results.html", illness=illness)

@app.route("/self_diagnose", methods=["GET", "POST"])
@login_required
def self_diagnose():
    if request.method == "POST":
        # add user's illness to database

        query = """UPDATE users SET illness = ('%s') WHERE id = (%s)"""
        info = (request.form.get("illness"), session.get("user_id"))
        
        conn = psycopg2.connect(DATABASE_URI)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        add_illness = cur.execute(query % info)

        conn.commit()
        return redirect("/")
    else:
        return render_template("self_diagnose.html")
  
@app.route("/travel_inquiry", methods=["GET","POST"])
def travel_inquiry():
  if request.method == "POST":
    if request.form.get('yes') == None:
      return redirect("/")
    else:
      return redirect("/travel_plans")
  else:
    return render_template("travel_inquiry.html")

@app.route("/travel_plans", methods=["GET","POST"])
@login_required
def travel_plans():
  if request.method == "POST":
    # find user's record
    conn = psycopg2.connect(DATABASE_URI)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # add information into user's database
    location = request.form.get("location")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    query = """UPDATE users SET (location, start_date, end_date) = (%s,%s,%s) WHERE id = (%s)"""
    
   # query = """INSERT INTO users (location, start_date, end_date) VALUES (%s,%s,%s)"""
    info = (location, start_date, end_date, session.get("user_id"))

    cur.execute(query , info)
    conn.commit()

    return redirect("/")
    
  else:
    return render_template("travel_plans.html")
    
@app.route("/logout")
def logout():

    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

