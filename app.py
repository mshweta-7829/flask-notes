'''Flask app for Notes'''

from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, bcrypt
from forms import UserRegisterForm, UserLoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLCHEMY_ECHO'] = True

connect_db(app)


app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()

@app.route("/")
def redirect_to_register():
    """ Redirect to register route """

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def handle_register():
    """ Displays a register for if its a get method
        and if its a post method, collects data from form and encrypts the password
        and creates instance of user with new user details
        and adds to database """

    form = UserRegisterForm()
    
    # HYPOTHESIS: 

    if form.validate_on_submit():
        # form.username.errors.clear()
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        is_user_exists = User.query.filter(User.username == username) #User or Error, look for method to give user or None
        print(f'{is_user_exists}')

        if is_user_exists.one_or_none()  :
            form.username.errors.append("This username is exists")
            return render_template("register.html", form=form)

        else:
            user_details = User.register(username, password)
            
            new_user = User(
                username = user_details.username, 
                password = user_details.password,
                first_name= first_name, 
                last_name = last_name, 
                email = email)
            
            db.session.add(new_user)
            db.session.commit()

            return redirect("/secret")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET","POST"])
def show_login_form():
    """ Show login form"""

    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        #authenticate will return user or False
        auth = User.authenticate(username,password)
        if auth:
            # Save login to session
            session['user_id'] = auth.username
            return redirect(f"/users/{auth.username}")
        else: 
            form.username.errors = ["Bad name/password"]

    else:
        return render_template('/login.html', form=form)

@app.route("/logout")
def logout_user():
    """ Log user out and redirect to home page"""

    session.pop("user_id", None)

    return redirect("/")

@app.route("/secret")
def show_secret():
    """ Check that user is authorized; redirect if not"""
    if "user_id" not in session:
        flash("you must be logged in to view!") #flash only appears if we have a /secret resource
        return redirect("/")
    else:
        return f'You made it!'

@app.route("/users/<username>")
def show_user_info(username):
    """Display user information """

    user_details = User.query.get_or_404(username)

    if "user_id" in session:
        is_authorized = User.authorized(username, session["user_id"])

        if is_authorized:
            return render_template("user.html", user = user_details)
    else:
        flash("you must be logged in to view!")
        return redirect("/login")


    