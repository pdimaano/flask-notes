
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model for SQLAlchemy."""

    username = db.Column(db.String(20),
                        primary_key=True
    )

    password = db.Column(db.String(100),
                        nullable=False
    )

    email = db.Column(db.String(50),
                        nullable=False,
                        unique=True
    )

    first_name = db.Column(db.String(30),
                        nullable=False
    )

    last_name = db.Column(db.String(30),
                        nullable=False
    )