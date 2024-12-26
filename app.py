from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy import MetaData
from webforms import LoginForm, UserForm, PostForm, PasswordForm


# Create Flask Instance
app = Flask(__name__)

# Add database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key
app.config['SECRET_KEY'] = 'your_secret_key'  # Clé secrète pour CSRF

# Add Login managment
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # redirect to /login if @login_required

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# ?---- DATABASE GESTION ------
# Init db
metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

db = SQLAlchemy(app, metadata=metadata)
# add database migration automation, allowing simple migration of the db
# each time we change one of our db.Model
migrate = Migrate(app, db, render_as_batch=True)

# Create User's model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
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

# Create a blog post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.now())
    slug = db.Column(db.String(255))
# ?----------------------------


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check password
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Successful')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password')
        else:
            flash('Wrong username')

    return render_template('login.html', form=form)

# Log Out function
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

# Dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Page 1 : INDEX
@app.route('/', methods=['GET', 'POST'])
def home():
    # form = MyForm()
    # if form.validate_on_submit():
    #     return render_template('name.html', name = form.name.data)
    return render_template('index.html')


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
@login_required
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

# PAGE : All BLOG posts
@app.route('/posts')
def posts():
    # Get all posts from db
    posts = Posts.query.order_by(Posts.date_posted)

    return render_template('posts.html',
                            posts=posts)

# PAGE Select one blog post to see
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

# DELETE Blog post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        # delete post from db
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Post Deleted !')
        # return all posts from db
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',
                            posts=posts)
    except:
        flash('Oops Try Again !')
        # return all posts from db
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',
                            posts=posts)

# PAGE Edit blog post
@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    
    if form.validate_on_submit():
        post.author = form.author.data
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data

        # Update db
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated !")
        return redirect(url_for('post', id=post.id))

    # fill form with post informations
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content

    return render_template('edit_post.html', form=form)


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
            user = Users(name=form.name.data,
                        email=form.email.data,
                        password_hash=hashed_pw,
                        username=form.username.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        # Clear form
        form.name.data = ''
        form.email.data = ''
        form.username.data = ''
        form.password_hash = ''
        flash('User add succesfully')
    our_users = Users.query.order_by(Users.date_added)

    return render_template('add_user.html',
                            form=form,
                            name=name,
                            our_users=our_users)

# Update user DB record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
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



