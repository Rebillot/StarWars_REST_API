from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
 
    def serialize(self):
        return {"id": self.id, "username": self.username}

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,

        }


class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,

        }


class Starships(db.Model):
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
