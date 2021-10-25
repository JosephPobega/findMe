from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.secret_key = "shhh"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.now)

@app.route('/')
def index():
    if 'user' in session:
        return "Logged in as " + session['user']
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':#handle form
        email = request.form['email']#get username from form
        existing_user = User.query.filter_by(email=email).first()#find the first user that matches name
        if existing_user:#check if user exists
            #hash the password and compare it to the one stored in the db
            existing_pass = existing_user.password
            if bcrypt.checkpw(request.form['pass'].encode('utf-8'), existing_pass.encode('utf-8')):
                #create session
                print('bro??')
                session['user'] = request.form['email']
                return redirect(url_for('index'))
        else:
            print('wrong username or password')
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #find existing user
        email = request.form['email']
        existing_user = User.query.filter_by(email=request.form['email']).first()
        #if there's no previous users let them sign up
        if existing_user is None:
            #hashed password
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            #creates a new user in table
            #i think its saying INSERT USER in USERS
            #tbh it's been a year since i looked at sql
            user = User(first_name=request.form['firstName'], last_name=request.form["lastName"], email=email, password=hashpass)
            #this prepares the user to be added to the table
            db.session.add(user)
            #commit new user to table
            db.session.commit()
            session['user'] = email
            print('user added')
            return redirect(url_for('index'))
        else:
            print('user exists')
    return render_template("register.html")

if __name__ == '__main__':
  app.run(debug=True)