from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, PasswordField, BooleanField, TextAreaField,ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate


# Create Flask Instance
app = Flask(__name__)

# Add database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key
app.config['SECRET_KEY'] = 'your_secret_key'  # Clé secrète pour CSRF

# Init db
db = SQLAlchemy(app)
# add database migration automation, allowing simple migration of the db
# each time we change one of our db.Model
migrate = Migrate(app, db)

# Create User's model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now())

    # Add password authentification
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String (equivalent of toString methods in Java)
    def __repr__(self):
        return '<Name %r>' % self.name

# Form for User
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit user')
    password_hash = PasswordField('Password',
                                  validators=[DataRequired(), EqualTo('password_hash2', message='Passwords not matching')])
    password_hash2 = PasswordField('Confirm Password',
                                   validators=[DataRequired()])

# Create a blog post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.now())
    slug = db.Column(db.String(255))

# Create a Post Form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Submit Post')

# Form for Name and Birthday to say hello
class MyForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()])
    birthday = DateField('Birthday',
                         format='%Y-%m-%d', validators=[DataRequired()])

    submit = SubmitField('Submit form')

# Form to check password
class PasswordForm(FlaskForm):
    email = StringField('Email',
                       validators=[DataRequired()])
    password_hash  = PasswordField('Password',
                             validators=[DataRequired()])
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

# PAGE 3 : Test Password
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None # is check valid or not

    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        
        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''

        # Check password
        # Lookup users by email address
        pw_to_check = Users.query.filter_by(email=email).first()
        passed = check_password_hash(pw_to_check.password_hash, password)

        # flash('Form Submitted succesfully !', category="info")

    return render_template('test_pw.html',
                            form = form,
                            email = email,
                            password = password,
                            pw_to_check = pw_to_check,
                            passed = passed)

# PAGE 4 : Post PAGE
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(
            author = form.author.data,
            title = form.title.data,
            content = form.content.data,
            slug = form.slug.data,
        )
        # Clear form
        form.title.data = ''
        form.author.data = ''
        form.slug.data = ''
        form.content.data = ''

        # Add post to db
        db.session.add(post)
        db.session.commit()

        flash('Post submitted')

    # Redirect to webpage
    return render_template('add_post.html', form=form)

# PAGE : BLOG posts
@app.route('/posts')
def posts():
    # Get all posts from db
    posts = Posts.query.order_by(Posts.date_posted)

    return render_template('posts.html',
                            posts=posts)

# PAGE USER/ADD
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        # get first user with same email address
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash password
            hashed_pw = generate_password_hash(form.password_hash.data)
            # Add user to db
            user = Users(name=form.name.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        # Clear form
        form.name.data = ''
        form.email.data = ''
        form.password_hash = ''
        flash('User add succesfully')
    our_users = Users.query.order_by(Users.date_added)

    return render_template('add_user.html',
                            form=form,
                            name=name,
                            our_users=our_users)


# Update DB record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template('update.html',
                                    form = form,
                                    name_to_update = name_to_update,
                                    id = id)
        except:
            flash("Error")
            return render_template('update.html',
                                    form = form,
                                    name_to_update = name_to_update,
                                    id = id)
        
    else:
        return render_template('update.html',
                                form = form,
                                name_to_update = name_to_update,
                                id = id )


@app.route('/delete<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("user deleted successfully")

        our_users = Users.query.order_by(Users.date_added)

        return render_template('add_user.html',
                            form=form,
                            name=name,
                            our_users=our_users)
    except:
        flash('oops error')
        
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



