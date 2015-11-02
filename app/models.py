# -- coding: utf-8 --
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, index=True)
    related_user1 = db.Column(db.Integer)
    related_user2 = db.Column(db.Integer)
    nickname = db.Column(db.UnicodeText(80), index=True, unique=True)
    phone = db.Column(db.String(50))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    waiting = db.relationship('Temp', backref='registrant', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Temp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    related_phone = db.Column(db.String(50))

    def __repr__(self):
        return '<Temp %r>' % (self.related_phone)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
