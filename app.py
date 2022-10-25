
from flask import Flask, request, redirect, render_template
from models import db, connect_db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get("/")
def redirect_to_register():
    """Redirect site visitor to register page."""

    return redirect("/register")


@app.get("/register")
def redirect_to_register():
    """Show a form that when submitted will register/create a user."""

    return render_template("register.html")