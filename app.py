from os import error
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from form import LoginForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, TextAreaField
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
    pfp_placement = db.Column(db.String(), default="center")
    bio_placement = db.Column(db.String(), default="center")
    post_placement = db.Column(db.String(), default="center")
    bio = db.Column(db.String(), default="BIO HERE")
    darkMode = db.Column(db.Boolean, default = True)

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
    user_id = db.Column(db.Integer, unique=False)
    post_title = db.Column(db.String(300), unique=False)
    post_content = db.Column(db.String(2800), unique=False) 
    profile_pic = db.Column(db.Boolean, default=False)  
    post_username = db.Column(db.String(30))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class PostForm(FlaskForm): 
    content = TextAreaField('content', validators=[InputRequired(), Length(max=2800)])
    title = StringField('title', validators=[InputRequired(), Length(max=300)] )

class EditProfileForm(FlaskForm): 
    profile_pic_placement = RadioField('profile_pic_placement', validators=[InputRequired()], choices = ['template1', 'template2', 'template3', 'template4', 'template5', 'template6'])

class EditUsername(FlaskForm): 
    username_change = StringField("username_change", validators=[InputRequired(), Length(min=4,max=15)])

class EditBio(FlaskForm):
    bio_change = StringField("bio_change", validators=[InputRequired(), Length(min=4,max=300)])

class SearchForm(FlaskForm): 
    searchword = StringField("searchword",validators=[InputRequired(), Length(min=4,max=15)])   

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
    return redirect('/')

@app.route('/whoisuser')
@login_required
def whoisuser(): 
    return "the current user is: "+  current_user.username

@app.route('/homefeed', methods=['POST', "GET"])
@login_required
def homefeed():
    form1 = SearchForm()
    title="'s Homefeed"
    username = current_user.username
    postz = Post.query.all()
    tenposts = postz[-10:]
    if request.method == "POST": 
        content = request.form.get("content")
        title = request.form.get("title")
        user_id = current_user.id
        new_post = Post(user_id = user_id, post_content = content, post_title=title, profile_pic = False, post_username = current_user.username)
        db.session.add(new_post)
        db.session.commit()
        postz = Post.query.all()
        tenposts = postz[-10:]
        return render_template("homefeed.html", title=current_user.username + "'s Homefeed", username=username, post1 = reversed(tenposts), form1=form1)
    return render_template("homefeed.html", title=(current_user.username + title), username=username, post1=reversed(tenposts), form1=form1 )


@app.route("/profile")
@login_required
def profile(): 
    return redirect('/profile/' + current_user.username)

@app.route("/profile/<username>")
@login_required
def profile2(username): 
    title="Profile Page"
    form1 = SearchForm()

    if current_user.username == username: 
        person = User.query.filter_by(username=current_user.username).first()
        posts= Post.query.filter_by(user_id = person.id).all()
        pfpalignment= person.pfp_placement
        bio = person.bio
        return render_template("profilePage.html", title=title, username=username, profileusername=username, posts=reversed(posts), pfp = pfpalignment, bio = bio, form1=form1)
    else: 
        person = User.query.filter_by(username=username).first()
        posts= Post.query.filter_by(user_id = person.id).all()
        pfpalignment = person.pfp_placement
        bio = person.bio
        return render_template("profilePage.html", title=title, profileusername=username,username=current_user.username, posts=reversed(posts),pfp = pfpalignment, bio=bio, form1=form1)

@app.route("/settings")
@login_required
def settings(): 
    return redirect('/settings/' + current_user.username)

@app.route("/settings/<username>")
@login_required
def settings2(username): 
    title="Settings Page"
    form1 = SearchForm()
    if current_user.username == username: 
        return render_template("settings.html", title=title, username=username, dm =current_user.darkMode, form1=form1)
    return "ah ah ah this isn't your account you bootyhole"

@app.route("/create")
@login_required
def create(): 
    title="create post"
    form = PostForm()
    form1 = SearchForm()

    return render_template("create.html", title=title, form=form, username=current_user.username, form1=form1)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/homefeed')
    form = RegisterForm()
    form1 = SearchForm()
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
            return render_template("homefeed.html", title=current_user.username + "'s homefeed", username=username,form1=form1 )
    return render_template('newProfile.html', form=form)
    

@app.route("/editprofile", methods=["GET", "POST"])
@login_required
def editprofile(): 
    form1 = SearchForm()
    title="Edit your profile!!"
    form = EditProfileForm()
    return render_template("editProfileForm.html", title=title, form=form, username=current_user.username, form1=form1)

@app.route("/update-profile", methods=["GET", "POST"])
@login_required
def update_profile(): 
    pfp = request.form.get('profile_pic_placement')
    posts = request.form.get('post_placement')
    bio = request.form.get("bio_placement")
    user = User.query.filter_by(id=current_user.id).first()
    user.pfp_placement = pfp
    user.bio_placement = bio
    user.post_placement = posts
    db.session.commit()
    return redirect('/profile')

@app.route("/darkmode")
@login_required
def darkmode():
    current_dm = current_user.darkMode
    if current_dm:
        current_user.darkMode = False
    else: 
        current_user.darkMode = True
    db.session.commit()
    return redirect('/settings')

@app.route("/editusername", methods=["GET", "POST"])
@login_required
def editusername(): 
    form1 = SearchForm()
    title="Edit your username!!"
    form = EditUsername()
    return render_template("editUsername.html", title=title, form=form, username=current_user.username, form1=form1)

@app.route("/edityourbio", methods=["GET", "POST"])
@login_required
def edityourbio(): 
    form1 = SearchForm()
    title="Edit your bio!!"
    form = EditBio()
    return render_template("editBio.html", title=title, form=form, username=current_user.username, form1=form1)

@app.route("/update-username", methods=["GET", "POST"])
@login_required
def update_username(): 
    user = User.query.filter_by(id=current_user.id).first()
    username = request.form.get("username_change")
    user.username = username
    db.session.commit()
    return redirect('/profile')

@app.route("/update-bio", methods=["GET", "POST"])
@login_required
def update_bio(): 
    user = User.query.filter_by(id=current_user.id).first()
    bio = request.form.get("bio_change")
    user.bio = bio
    db.session.commit()
    return redirect('/profile')

@app.route('/search', methods=["POST", "GET"])
@login_required
def searchdb(): 
    form1 = SearchForm()
    formword = request.form.get('searchword')
    user = User.query.filter_by(username=str(formword)).first()
    if user: 
        return render_template("showSearch.html", user = user, username = current_user.username, form1=form1)
    return render_template("showNoPeople.html", form1=form1, username= current_user.username)

@app.route('/searchprofile/<username>')
@login_required
def searchprofile(username): 
    return redirect('/profile/' + username)

@app.route('/clickedpost/<id>', methods=["GET"])
@login_required
def clickedpost(id): 
    form1 = SearchForm()
    postz = Post.query.filter_by(id = id).first()
    post_user = User.query.filter_by(id=postz.user_id).first()

    return render_template('clickedpost.html', form1=form1, username = current_user.username, postz = postz, post_user=post_user)

@app.route('/deleteaccount')
@login_required
def deleteaccount(): 
    user = User.query.filter_by(id = current_user.id).first()
    posts = Post.query.filter_by(user_id = current_user.id).all()
    for post in posts: 
        db.session.delete(post)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/deleteconfirm')
@login_required
def deleteconfirm(): 
    form1 = SearchForm()
    title = "Confirm Account Delete"
    return render_template('deleteConfirm.html', title=title, form1=form1, username = current_user.username)