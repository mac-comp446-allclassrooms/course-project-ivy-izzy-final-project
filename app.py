from os import error
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from form import LoginForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)

#initialize the login-- Used a tutorial from https://www.youtube.com/watch?v=2dEM-s3mRLE
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String())
    is_authenticated = db.Column(db.Boolean, default=False)
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def setUsername(self,username):
        self.username = username
    
    def setEmail(self, email): 
        self.email = email

class Post(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@login_manager.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect('/homefeed')
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        usernamesmatch = user.username == username
        passwordsmatch = user.check_password(password)
        if usernamesmatch and passwordsmatch:
            login_user(user)
            user.is_authenticated=True
            db.session.add(user)
            db.session.commit()
            return redirect('/homefeed')
        return '<h1>Invalid username or password</h1>'
    return render_template('index.html', form=form)
    
@app.route('/logout')
@login_required
def logout():
    db.session.add(current_user)
    db.session.commit()
    logout_user()
    return("You've been logged out!")

@app.route('/whoisuser')
@login_required
def whoisuser(): 
    return "the current user is: "+  current_user.username

@app.route('/homefeed', methods=['POST', "GET"])
@login_required
def homefeed():
    return redirect('/homefeed/'+current_user.username)

@app.route('/homefeed/<username>', methods=['POST', "GET"])
@login_required
def homefeed2(username):
    title="'s Homefeed"
    if request.method == "POST": 
        return render_template("homefeed.html", title=current_user.username + title, username=username)
    return render_template("homefeed.html", title=(current_user.username + title), username=username )

@app.route("/profile")
@login_required
def profile(): 
    return redirect('/profile/' + current_user.username)

@app.route("/profile/<username>")
@login_required
def profile2(username): 
    title="Profile Page"
    return render_template("profilePage.html", title=title, username=username)

@app.route("/settings")
@login_required
def settings(): 
    return redirect('/settings/' + current_user.username)

@app.route("/settings/<username>")
@login_required
def settings2(username): 
    title="Settings Page"
    return render_template("settings.html", title=title, username=username)

@app.route("/create")
@login_required
def create(): 
    title="create post"
    return render_template("create.html", title=title)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/homefeed')
    form = RegisterForm()

    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get('password')
        email = request.form.get('email')

        usernameindb = User.query.filter_by(username=username).first()
        emailindb = User.query.filter_by(email=email).first()
        if usernameindb:
            return "<h1> This username is already taken! </h1>"
        elif emailindb: 
            return "<h1> This email already has an account associated with it!</h1>"
        else: 
            new_user = User(username = username, email=email)
            new_user.set_password(password)
            new_user.is_authenticated=True
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return render_template("homefeed.html", title=current_user.username + "'s homefeed", username=username )
    return render_template('newProfile.html', form=form)
    