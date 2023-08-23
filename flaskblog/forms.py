# Importing necessary classes and modules
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

# Defining the RegistrationForm class, which inherits from FlaskForm


class RegistrationForm(FlaskForm):
    # Defining form fields and associated validators
    username = StringField('username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[
                                     DataRequired(), EqualTo('password')])
    # Submit button for the form
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Username taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken. Please choose a different one')

# Defining the LoginForm class, which also inherits from FlaskForm


class LoginForm(FlaskForm):
    # Defining form fields and associated validators
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Checkbox field for remembering login
    remember = BooleanField('Remember Me')
    # Submit button for the form
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    # Defining form fields and associated validators
    username = StringField('username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])

    # Submit button for the form
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'Username taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'Email taken. Please choose a different one')
