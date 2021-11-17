from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
#initialize the database
db = SQLAlchemy(app)

#create a db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r' % self.id

@app.route("/friends", methods=['POST', 'GET'])
def friends():
    title = "My Friends List, yay!"

    if request.method == "POST":
        # add to database
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)
        # push into database

        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error adding this to the database..."
    
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template('friends.html', title=title, friends=friends)
    
@app.route("/")
def index():
    title = "Login!"
    return render_template("index.html", title=title)


#example of a page which can be a form
#you can add an HTTP method such as post for data
#there are request and response objects in flask
@app.route("/homefeed", methods=["POST"])
def homefeed():
    title="Homefeed"
    return render_template("homefeed.html", title=title)


@app.route("/profile")
def profile(): 
    title="Profile Page"
    return render_template("profilePage.html", title=title)

@app.route("/settings")
def settings(): 
    title="Settings Page"
    return render_template("settings.html", title=title)