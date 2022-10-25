
from flask import Flask, request, redirect, render_template, session
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get("/")
def homepage():
    """Redirects user to registration page."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def user_registration():
    """ Handles user registration. Displays HTML form, and
    registers new users on form submission.

    On successful registration, redirects to /secret page.
    Else, re-render the HTML with any validation errors."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        # add User class method for registering user
        user = User.register(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        db.commit()
        session['username'] = user.username

        return redirect('/secret')

    else:
        return render_template(
            "register.html",
            form=form)


@app.route('/login', methods=['GET', 'POST'])
def user_login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect('/secret')

        else:
            form.username.errors = ['Incorrect username/password combination']

    return render_template('login.html', form=form)


@app.get('/secret')
def show_secret():
    """ Shows the secret page """

    return render_template('secret.html')
