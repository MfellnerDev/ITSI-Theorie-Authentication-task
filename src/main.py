from flask import Blueprint, render_template, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

app.config["SECRET_KEY"] = "SECRET-KEY"

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app')
def app():
    return render_template('app.html')

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    favourite_color = db.Column(db.String(100))

db.init_app(app)

with app.app_context():
    db.create_all()