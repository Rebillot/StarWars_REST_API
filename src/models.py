from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable= False, unique = True)
    password = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable=False)
    

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    homeworld_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    starship = db.Column(db.Integer, db.ForeignKey("starship.id"), nullable=False)


class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(50), nullable=False)
    rotation = db.Column(db.Integer, nullable=False)


class Starships(db.Model):
    __tablename__ = "starship"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    starship_class = db.Column(db.String(50), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    pilots = db.Column(db.String, db.ForeignKey("character.id"), nullable=True)


class Favorites(db.Model):
    __tablename__ = "favorites"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    starship_id = db.Column(db.Integer, db.ForeignKey("starship.id"), nullable=False)
