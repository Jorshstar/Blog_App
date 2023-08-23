import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flaskblog import db
from flask_bcrypt import Bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
# Importing necessary modules and classes from Flask
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# Sample data for blog posts
posts = [
    {
        '_author': 'Joshua Akinbode',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        '_author': 'Jaxon Darter',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 24, 2018'
    }
]

# Route decorators to define URL endpoints and associated functions

main = Blueprint('main', __name__)
bcrypt = Bcrypt()


@main.route("/")
@main.route("/home")
def home():
    print("Home route triggered!")
    # Rendering 'home.html' template with the 'posts' data
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    print("About route triggered!")
    # Rendering 'about.html' template with a title
    return render_template('about.html', title='About')


@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # Creating an instance of the RegistrationForm class
    form = RegistrationForm()
    # Checking if the form was submitted and validated
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # Displaying a success message
        flash('Your account has been created! You are now able to login', 'success')
        # Redirecting to the 'home' route
        return redirect(url_for('main.login'))
    # Rendering 'register.html' with the form
    return render_template('register.html', title='Register', form=form)


@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # Creating an instance of the LoginForm class
    form = LoginForm()
    # Checking if the form was submitted and validated
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # Displaying an error message
            flash('Login Unsuccessful. Please check email and password', 'danger')
            # Rendering 'login.html' with the form
    return render_template('login.html', title='Login', form=form)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        main.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@main.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
