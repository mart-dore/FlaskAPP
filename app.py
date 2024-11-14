from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create Flask Instance
app = Flask(__name__)

# Add database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key
app.config['SECRET_KEY'] = 'your_secret_key'  # Clé secrète pour CSRF

# Init db
db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now())

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name
    
# Form for User
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit user')


# Form for name test
class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit form')


# Page 1 : INDEX
@app.route('/', methods=['GET', 'POST'])
def home():
    # form = MyForm()
    # if form.validate_on_submit():
    #     return render_template('name.html', name = form.name.data)
    return render_template('index.html')

# PAGE 2 : FORM
@app.route('/form', methods=['GET', 'POST'])
def form():
    name = None
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash('Form Submitted succesfully !', category="info")

    return render_template('form.html',
                            form = form,
                            name = name)


# PAGE USER/ADD
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        # get first user with same email address
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # add user to db
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        # Clear form
        form.name.data = ''
        form.email.data = ''
        flash('User add succesfully')
    our_users = Users.query.order_by(Users.date_added)

    return render_template('add_user.html',
                            form=form,
                            name=name,
                            our_users=our_users)


# PAGE USER/NAME
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# ERRORS
# Invalid URL / Pagename
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Servor Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)



