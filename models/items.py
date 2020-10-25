from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Items(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.String(80), unique=True, nullable=False)