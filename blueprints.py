from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listens_for
from flask_bcrypt import Bcrypt
from models import Users, Comments
from database import db
from flask_login import login_user, login_required, logout_user, current_user
from better_profanity import profanity
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms.fields.simple import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

blueprints = Blueprint(__name__, "blueprints")

bcrypt = Bcrypt()

class comments_form(FlaskForm):
    comment = TextAreaField("Leave a new comment", validators = [DataRequired(message = "Comment cannot be empty"), Length(max = 1000, message = 'Comment cannot be longer than 1000 characters')
    ], render_kw = {"rows": 4, "style": "width: 100%;", "placeholder": "Enter new comment here"})
    submit = SubmitField("Add Comment", render_kw = {"class": "comment-form-button"})

def process_comment(form):
    if request.method == "POST":
        if profanity.contains_profanity(form.comment.data):
            flash("Comment contains profanity and cannot be posted", category = "form_error")
        else:
            new_comment = Comments(text = form.comment.data, user_name = current_user.name)
            db.session.add(new_comment)
            try:
                db.session.commit()
                flash("Comment added successfully!", category = "form_success")
                form.comment.data = ""
                redirect(url_for("blueprints.home"))
            except Exception as e:
                db.session.rollback()
                print(e)
                flash("An error occurred. Please try again.", category = "form_error")
        form.comment.data = ""

def flash_errors(form):
    for field in form:
        for error in field.errors:
            flash(f"{error}", category = "form_error")

@blueprints.route('/', methods = ["GET", "POST"])
@login_required
def home():
    form = comments_form()
    header = "Welcome to my Portfolio"
    if form.validate_on_submit():
        process_comment(form)
    else:
        flash_errors(form)
    comments = Comments.query.all()
    title = "Home"
    return render_template("index.html", title = title, header = header, user = current_user, comments = comments, form = form)

@blueprints.route("/login", methods = ["GET", "POST"])
def login():
    form = comments_form()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email = email).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, password):
                flash(f"Login successful! Welcome, {user.name}!", category = "form_success")
                login_user(user, remember = True)
                return redirect(url_for("blueprints.home"))
            else:
                flash("Incorrect password.", category = "form_error")
        else:
            flash("Email does not exist.", category = "form_error")

    title = "Login"
    return render_template("login.html", header = title, title = title, user = current_user, form = form)

@blueprints.route("/signup", methods = ["GET", "POST"])
def signup():
    form = comments_form()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("confirm-password")
        user = Users.query.filter_by(email = email).first()
        if user:
            flash("Email already exists", category = "form_error")
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
    return render_template("signup.html", header = "Create New User Account", title = title, user = current_user, form = form)

@blueprints.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out", category = "form_success")
    return redirect(url_for("blueprints.login"))

@blueprints.route("/about", methods = ["GET", "POST"])
@login_required
def about():
    form = comments_form()
    if form.validate_on_submit():
        process_comment(form)
    else:
        flash_errors(form)
    comments = Comments.query.all()
    title = "About Me"
    return render_template("about.html", header = title, title = title, user = current_user, comments = comments, form = form)

@blueprints.route("/experience", methods = ["GET", "POST"])
@login_required
def experience():
    form = comments_form()
    if form.validate_on_submit():
        process_comment(form)
    else:
        flash_errors(form)
    comments = Comments.query.all()
    title = "My Experience"
    return render_template("experience.html", header = title, title = title, user = current_user, comments = comments, form = form)

@blueprints.route("/projects", methods = ["GET", "POST"])
@login_required
def projects():
    form = comments_form()
    if form.validate_on_submit():
        process_comment(form)
    else:
        flash_errors(form)
    comments = Comments.query.all()
    title = "My Projects"
    return render_template("projects.html", header = title, title = title, user = current_user, comments = comments, form = form)
