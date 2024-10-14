from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template("login.html")

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/home")
def homepage():
    return render_template("home.html")

@auth.route("/login", methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    print(email, password)

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for("auth.login"))
    
    print(email, password)

    return redirect(url_for("auth.homepage"))

@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=['POST'])
def signup_post():
    email = request.form['email']
    password = request.form['password']
    rollno = request.form['rollno']
    dept = request.form['dept']
    name = request.form['name']
    gender = request.form['gender']

    print(rollno, name, dept, gender, email, password)

    user = User.query.filter_by(email=email).first()

    if user:
        print("User already exists")
    
    new_user = User(email = email, name = name, password = generate_password_hash(password),
                    id = rollno, gender = gender, dept = dept, role ="USER")
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))
