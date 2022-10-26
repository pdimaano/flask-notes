
from flask import Flask, redirect, render_template, session, flash
from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm, EditNoteForm
from flask_debugtoolbar import DebugToolbarExtension

from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Secret Something'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.get("/")
def homepage():
    """Redirects user to registration page."""

    return redirect("/register")

########################    USER    ##############################


@app.route("/register", methods=["GET", "POST"])
def user_registration():
    """ Handles user registration. Displays HTML form, and
    registers new users on form submission.

    On successful registration, redirects to /users/username page.
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
        db.session.commit()
        session['username'] = user.username

        return redirect(f'/users/{username}')

    else:
        return render_template(
            "register.html",
            form=form)


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    """Show a form that when submitted will login a user."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{username}')

        else:
            form.username.errors = ['Incorrect username/password combination']

    return render_template(
        'login.html',
        form=form)


@app.get('/users/<username>')
def show_user_page(username):
    """ Shows the user page only for logged in users. """

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    if "username" not in session:
        flash("You must be logged in to view this page.")
        return redirect("/")

    if username != session["username"]:
        raise Unauthorized()

    else:
        return render_template(
            'user.html',
            user=user,
            form=form)


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect("/")


@app.post("/users/<username>/delete")
def delete_account(username):
    """Deletes user account and redirects to the homepage."""

    form = CSRFProtectForm()

    if "username" not in session:
        flash("You must be logged in to view this page.")
        return redirect("/")

    if username != session["username"]:
        raise Unauthorized()

    if form.validate_on_submit():
        session.pop("username", None)

    User.delete_account(username)

    return redirect("/")


########################    NOTES    ##############################


@app.route('/users/<username>/notes/add', methods=['GET', 'POST'])
def add_note(username):
    """ Adds a new note for a user """

    if username != session["username"]:
        raise Unauthorized()

    form = AddNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        owner = username

        note = Note(
            title=title,
            content=content,
            owner=owner)

        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template(
            'note_add.html',
            form=form)


@app.route('/notes/<note_id>/update', methods=['GET', 'POST'])
def edit_note(note_id):
    """ Edit an already existing note for a user """

    note = Note.query.get_or_404(note_id)
    form = EditNoteForm(obj=note)

    if note.owner != session["username"]:
        raise Unauthorized()

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{note.owner}')

    else:
        return render_template(
            'note_edit.html',
            form=form, note=note)


@app.post("/notes/<note_id>/delete")
def delete_note(note_id):
    """Deletes note and redirects to user detail page."""
    #TODO: CSRF validation

    note = Note.query.get_or_404(note_id)
    if note.owner != session["username"]:
        raise Unauthorized()

    db.session.delete(note)
    db.session.commit()

    return redirect(f"/users/{note.owner}")
