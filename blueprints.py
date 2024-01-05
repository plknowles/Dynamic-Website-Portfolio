from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import Users, Comments
from database import db
from flask_login import login_user, login_required, logout_user, current_user
from better_profanity import profanity

blueprints = Blueprint(__name__, "blueprints")

bcrypt = Bcrypt()

@blueprints.route('/', methods = ["GET", "POST"])
@login_required
def home():
    header = "Welcome to my Portfolio"
    comments = Comments.query.all()
    if request.method == "POST":
        input_comment = request.form.get("comment")
        if len(input_comment) == 0:
            flash("Comment cannot be empty", category = "form_error")
        elif profanity.contains_profanity(input_comment):
            flash("Comment contains profanity and cannot be posted", category = "form_error")
        else:
            new_comment = Comments(text = input_comment, name = current_user.name)
            db.session.add(new_comment)
            try:
                db.session.commit()
                flash("Comment added successfully!", category = "form_success")
                return redirect(url_for("blueprints.home"))
            except Exception as e:
                db.session.rollback()
                print(e)
                flash("An error occurred. Please try again.", category = "form_error")
    title = "Home"
    return render_template("index.html", title = title, header = header, user = current_user, comments = comments)

@blueprints.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email = email).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, password):
                flash(f"Login successful! Welcome, {user.name}!", category="form_success")
                login_user(user, remember = True)
                return redirect(url_for("blueprints.home"))
            else:
                flash("Incorrect password.", category="form_error")
        else:
            flash("Email does not exist.", category="form_error")

    title = "Login"
    return render_template("login.html", header = title, title = title, user = current_user)

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
    return render_template("signup.html", header = "Create New User Account", title = title, user = current_user)

@blueprints.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out", category="form_success")
    return redirect(url_for("blueprints.login"))

@blueprints.route("/search")
@login_required
def search():
    title = "Site Search"
    return render_template("search.html", header = title, title = title, user = current_user)

@blueprints.route("/about")
@login_required
def about():
    title = "About Me"
    return render_template("about.html", header = title, title = title, user = current_user)

@blueprints.route("/experience")
@login_required
def experience():
    title = "My Experience"
    return render_template("experience.html", header = title, title = title, user = current_user)

@blueprints.route("/projects")
@login_required
def projects():
    title = "My Projects"
    return render_template("projects.html", header = title, title = title, user = current_user)