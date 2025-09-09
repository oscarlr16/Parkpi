from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    decision = db.Column(db.String)
    msg = db.Column(db.String)
