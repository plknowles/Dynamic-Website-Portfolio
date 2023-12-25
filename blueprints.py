from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import Users, Comments
from database import db

blueprints = Blueprint(__name__, "blueprints")

bcrypt = Bcrypt()

@blueprints.route('/')
def home():
    header = "Welcome to my Portfolio"
    title = "Home"
    return render_template("index.html", title = title, header = header)

@blueprints.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email = email).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, password):
                flash(f"Login successful! Welcome, {user.name}!", category="form_success")
                return redirect(url_for("blueprints.home"))
            else:
                flash("Incorrect password.", category="form_error")
        else:
            flash("Email does not exist.", category="form_error")

    title = "Login"
    return render_template("login.html", header = title, title = title)

@blueprints.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("confirm-password")
        
        user = Users.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category="form_error")

        elif len(email) < 4:
            flash("Email must be at least 4 characters in length.", category = "form_error")
        elif len(name) < 2:
            flash("Name must be at least 2 characters in length.", category = "form_error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters in length.", category = "form_error")
        elif password != password_confirm:
            flash("Passwords don't match.", category = "form_error")
        else:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = Users(email = email, name = name, password_hash = password_hash)
            db.session.add(new_user)
            try:
                db.session.commit()
                flash("Account created successfully. Please log in.", category = "form_success")
                return redirect(url_for("blueprints.login"))
            except Exception as e:
                db.session.rollback()
                print(e)
                flash("An error occurred during account creation. Please try again.", category = "form_error")

    title = "Create Account"
    return render_template("signup.html", header = "Create New User Account", title = title)

@blueprints.route("/logout")
def logout():
    title = "Logout"
    return render_template("logout.html", header = title, title = title)

@blueprints.route("/search")
def search():
    title = "Site Search"
    return render_template("search.html", header = title, title = title)

@blueprints.route("/about")
def about():
    title = "About Me"
    return render_template("about.html", header = title, title = title)

@blueprints.route("/experience")
def experience():
    title = "My Experience"
    return render_template("experience.html", header = title, title = title)

@blueprints.route("/projects")
def projects():
    title = "My Projects"
    return render_template("projects.html", header = title, title = title)