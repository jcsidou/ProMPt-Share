from app import db
from datetime import datetime

prompt_category = db.Table('prompt_category',
    db.Column('prompt_id', db.Integer, db.ForeignKey('prompt.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    text = db.Column(db.String(140))
    role = db.Column(db.String(10))
    temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Certifique-se de que é author_id
    categories = db.relationship('Category', secondary=prompt_category, backref=db.backref('prompts', lazy='dynamic'))

    def __repr__(self):
        return '<Prompt {}>'.format(self.name)
