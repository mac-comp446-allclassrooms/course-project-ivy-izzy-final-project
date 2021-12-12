from form import LoginForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm 
from werkzeug.security import generate_password_hash, check_password_hash

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