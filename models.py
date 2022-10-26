
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Individual User"""

    __tablename__ = 'users'

    # access list of user's notes
    notes = db.relationship('Note', backref='owner', cascade="all, delete")

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls,
                 username,
                 password,
                 first_name,
                 last_name,
                 email):
        """ Registers the user and hashes the password. """

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username,
                   password=hashed,
                   first_name=first_name,
                   last_name=last_name,
                   email=email)

    @classmethod
    def authenticate(cls,
                     username,
                     password):
        """ Validates that user exists & password is correct

        Return user if valid; else return False
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    @classmethod
    def delete_account(cls,
                       username):
        """ Removes a user from the database"""

        user = cls.query.filter_by(username=username).one_or_none()

        db.session.delete(user)
        db.session.commit()


class Note(db.Model):
    """ Individual Note """
    # access the note's author with note.owner

    __tablename__ = 'notes'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    owner = db.Column(db.String(20),
                      db.ForeignKey('users.username'),
                      nullable=False,
                      )
