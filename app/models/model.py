# app/models/model.py
from app import db

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    prompts = db.relationship('Prompt', backref='model', lazy='dynamic')
