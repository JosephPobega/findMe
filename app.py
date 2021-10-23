from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)

@app.route('/')
def index():
  return render_template("index.html")

if __name__ == '__main__':
  app.run(debug=True)