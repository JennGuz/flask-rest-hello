from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    is_dead = db.Column(db.Boolean(), unique=False, nullable=False)


    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "is_dead": self.is_dead
            # do not serialize the password, its a security breach
        }
    
   
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            # do not serialize the password, its a security breach
        }
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_id = db.Column(db.Integer, nullable=False)
    favorite_type = db.Column(db.String(80), nullable=False)

    user = db.relationship('User', backref=db.backref('favorites', lazy=True))

    def __init__(self, user_id, favorite_id, favorite_type):
        self.user_id = user_id
        self.favorite_id = favorite_id
        self.favorite_type = favorite_type
    
    def serialize(self):
        return {
            "user_id": self.user_id,
            "favorite_id": self.favorite_id,
            "favorite_type": self.favorite_type,
            # do not serialize the password, its a security breach
        }

