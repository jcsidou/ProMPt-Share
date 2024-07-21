from app import db

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'))
    score = db.Column(db.Integer)

    def __repr__(self):
        return '<Rating {}>'.format(self.score)
