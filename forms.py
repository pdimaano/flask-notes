
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    """Form to register/create a user."""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(
                max=20,
                message="Max length is 20 characters.")])

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(
                max=100,
                message="Max length is 100 characters.")])

    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email(),
            Length(
                max=50,
                message="Max length is 50 characters.")])

    first_name = StringField(
        "First Name",
        validators=[
            InputRequired(),
            Length(
                max=30,
                message="Max length is 30 characters.")])

    last_name = StringField(
        "Last Name",
        validators=[
            InputRequired(),
            Length(
                max=30,
                message="Max length is 30 characters.")])


class LoginForm(FlaskForm):
    """ Form to login user to the site """

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(
                max=20,
                message="Max length is 20 characters.")])

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(
                max=100,
                message="Max length is 100 characters.")])


class AddNoteForm(FlaskForm):
    " Form to add a note to a user's account"

    title = StringField(
        "Title",
        validators=[
            InputRequired(),
            Length(
                max=100,
                message="Max length is 100 characters.")]
    )

    content = TextAreaField(
        "Content",
        validators=[
            InputRequired()]
    )


class EditNoteForm(FlaskForm):
    " Form to edit a note to a user's account"

    title = StringField(
        "Title",
        validators=[
            InputRequired(),
            Length(
                max=100,
                message="Max length is 100 characters.")]
    )

    content = TextAreaField(
        "Content",
        validators=[
            InputRequired()]
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection."""
