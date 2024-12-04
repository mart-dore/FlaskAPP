from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, PasswordField, BooleanField, TextAreaField,ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea

# Form for User
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password_hash = PasswordField('Password',
                                  validators=[DataRequired(), EqualTo('password_hash2', message='Passwords not matching')])
    password_hash2 = PasswordField('Confirm Password',
                                   validators=[DataRequired()])
    submit = SubmitField('Update Profile')

# Create a Post Form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Submit Post')

# Create a Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) 
    password = PasswordField('Password',
                                   validators=[DataRequired()])
    submit = SubmitField('Login')
    pass

# Form to check password
class PasswordForm(FlaskForm):
    email = StringField('Email',
                       validators=[DataRequired()])
    password_hash  = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Submit form')

