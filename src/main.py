from flask import Blueprint, render_template, Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user

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


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        user = User(email=request.form.get('email'),
                    password=request.form.get('password'),
                    favorite_color=request.form.get('color'))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            email=request.form.get('email')).first()

        if user.password == request.form.get('password'):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')


if __name__ == "__main__":
    app.run()
