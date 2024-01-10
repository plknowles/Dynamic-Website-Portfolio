from flask import Blueprint, render_template, url_for, request, flash, redirect # Flask web framework: Pallets/flask: The Python Micro Framework for building web applications., GitHub. Available at: https://github.com/pallets/flask
from flask_sqlalchemy import SQLAlchemy # Facilitates database operations and has built-in support for parameterized queries, prevents SQL Injection. Sqlalchemy/sqlalchemy: The database toolkit for python, GitHub. Available at: https://github.com/sqlalchemy/sqlalchemy
from werkzeug.utils import escape # Sanitise comments to prevent HTML and JavaScript injection. Werkzeug WSGI web application library: Pallets/Werkzeug: The comprehensive WSGI web application library., GitHub. Available at: https://github.com/pallets/werkzeug/
from flask_bcrypt import Bcrypt # Hash passwords for improved data protection and security. Bcrypt password hashing: PYCA/bcrypt: Modern(-ish) password hashing for your software and your servers, GitHub. Available at: https://github.com/pyca/bcrypt
from models import Users, Comments
from database import db
from flask_login import login_user, login_required, logout_user, current_user # Manages user authentication, session tracking, and access control. Maxcountryman/flask-login: Flask User Session Management., GitHub. Available at: https://github.com/maxcountryman/flask-login
from better_profanity import profanity # Profanity filtering. Snguyenthanh/better_profanity: Blazingly fast cleaning swear words (and their leetspeak) in strings, GitHub. Available at: https://github.com/snguyenthanh/better_profanity
from flask_wtf import FlaskForm # WTFORMS/Flask-WTF: Simple integration of flask and WTFORMS, including CSRF, file upload and recaptcha integration., GitHub. Available at: https://github.com/wtforms/flask-wtf
from flask_wtf.csrf import CSRFProtect # Enable csrf protection for better security
from wtforms.fields.simple import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

# Create a Blueprint instance for routing
blueprints = Blueprint(__name__, "blueprints")

bcrypt = Bcrypt()

# FlaskWTF form to handle comments, enables csrf protection for better security
class comments_form(FlaskForm):
    # comment validators included by FlaskWTF
    comment = TextAreaField("Leave a new comment", validators = [DataRequired(message = "Comment cannot be empty"), Length(max = 1000, message = 'Comment cannot be longer than 1000 characters')
    ], render_kw = {"rows": 4, "style": "width: 100%;", "placeholder": "Enter new comment here"})
    submit = SubmitField("Add Comment", render_kw = {"class": "comment-form-button"})

# Process comment form submission
def process_comment(form):
    if request.method == "POST":
        # Sanitise the comment to prevent HTML and JavaScript injection
        sanitised_comment = escape(form.comment.data)
        # profanity sanitisation
        if profanity.contains_profanity(sanitised_comment):
            flash("Comment contains profanity and cannot be posted", category = "form_error")
        else:
            new_comment = Comments(text = sanitised_comment, user_name = current_user.name, user_id = current_user.id)
            db.session.add(new_comment)
            try:
                db.session.commit()
                flash("Comment added successfully!", category = "form_success")
                # clears the comment entry data if submitted and returns True
                form.comment.data = None
                return True
            except Exception as e:
                db.session.rollback()
                print(e)
                flash("An error occurred. Please try again.", category = "form_error")
        # returns false if comment not submitted
        return False

# Flash form errors/successes at the top of the page
def flash_errors(form):
    for field in form:
        for error in field.errors:
            flash(f"{error}", category = "form_error")

@blueprints.route('/', methods = ["GET", "POST"])
@login_required # decorator is part of Flask-Login extension and allows access only if user is authenticated
def home():
    form = comments_form()
    header = "Hi, I'm Peter &#128075"
    if form.validate_on_submit():
        if process_comment(form):
            # reloads current page if comment submitted
            return redirect(request.url)
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
        # form validation
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

    title = "Create New Account"
    return render_template("signup.html", header = "Create New Account", title = title, user = current_user, form = form)

@blueprints.route("/logout")
@login_required
def logout():
    logout_user() # Handled by Flask-Login
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

# route to handle comment deletion, comment id is passed in from deleteComment.js script
@blueprints.route("/comments/<int:comment_id>", methods=["DELETE"])
@login_required
def delete_comment(comment_id):
    try:
        comment = Comments.query.get(comment_id)

        if not comment:
            return "Comment not found", 404

        # prevents deletion of other user comments
        if current_user.id != comment.user_id:
            flash("You do not have permission to delete this comment.", category = "form_error")
            return "Permission denied", 403

        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted successfully.", category = "form_success")
        return "Comment deleted successfully", 204
    except Exception as e:
        print(f"An error occurred: {e}")
        flash("An error occurred while deleting the comment.", category = "form_error")
        return "An error occurred while deleting the comment", 500
