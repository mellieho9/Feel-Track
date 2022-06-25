#imports

import os 

# flask imports 

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

# DB import
import psycopg2
import psycopg2.extras


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

                return redirect("/survey")
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
        if request.form['1'] != "" or request.form['2'] != "":
            redirect("/health_survey")
        return redirect("/travel_inquiry")
    else:
        return render_template("emotional_survey.html")

@app.route("/health_survey", methods=["GET", "POST"])
def health_survey():
  if request.method == "POST":
    # convert symptoms string to list
    symptoms = request.form.get("symptoms")
    symptoms_list = symptoms.split(",")

    # add symptoms list into the user's database

    query = """INSERT INTO users (symptoms_list) VALUES (%s)"""
    info = (symptoms_list)
  else:
    return render_template("health_survey.html")
  
@app.route("/travel_inquiry", methods=["GET","POST"])
def travel_inquiry():
  if request.method == "POST":
    if request.form['yes'] != "":
      return redirect("/travel_plans")
    else:
      return redirect("/")
  else:
    return render_template("travel_inquiry.html")

@app.route("/travel_plans", methods=["GET","POST"])

def travel_plans():
  if request.method == "POST":
    # find user's record
    conn = psycopg2.connect(DATABASE_URI)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # add information into user's database
    location = request.form.get("location")
    start-date = request.form.get("start-date")
    end-date = request.form.get("end-date")
    
    query = """INSERT INTO users (location, start-date, end-date) VALUES (%s,%s,%s)"""
    info = (location, start-date, end-date)
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
