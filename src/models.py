from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

tabla_ch_favorites= db.Table(
    "ch_favorites",
    db.Column('User_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('Character_id', db.Integer, db.ForeignKey('character.id'))
)

tabla_Pl_favorites = db.Table(
    'Pl_favorites',
    db.Column('User_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('Planet_id', db.Integer, db.ForeignKey('planet.id'))
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    characters = db.relationship('Character', secondary = tabla_ch_favorites, back_populates='users')
    planets = db.relationship('Planet', secondary = tabla_Pl_favorites, back_populates='users')

    def serialize(self):
        return {"id": self.id, "username": self.username}

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', secondary = tabla_ch_favorites, back_populates='characters')


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,

        }


class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', secondary = tabla_Pl_favorites, back_populates='planets')


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,

        }


class Starship(db.Model):
    __tablename__ = "starship"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,

        }


# class Favorites(db.Model):
#     __tablename__ = "favorites"
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
#     character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
#     planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
#     starship_id = db.Column(db.Integer, db.ForeignKey("starship.id"), nullable=False)
