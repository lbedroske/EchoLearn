from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.Date, default=date.today)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=True)
    class_ref = db.relationship('Class', backref='topics')