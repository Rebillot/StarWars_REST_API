"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, abort
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Starship


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


################# USERS ###################

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.route('/user/<string:user_id>',methods=['GET'])
def get_single_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort (404)
    return jsonify(user.serialize())    

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    username = data['username']
    newUser = User(username=username)
    db.session.add(newUser)
    db.session.commit()
    return jsonify(newUser.serialize()), 201

@app.route('/user/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    selectUser = User.query.get(user_id)
    if selectUser is None:
        abort(404)
    selectUser.username = request.json['username']
    db.session.commit()
    return jsonify(selectUser.serialize())

@app.route('/user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    selectUser = User.query.get(user_id)
    if selectUser is None:
        abort(404)
    db.session.delete(selectUser)
    db.session.commit()
    return jsonify({'result': 'Success deleting'})


################# CHARACTERS ###################

@app.route('/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters])

@app.route('/character/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        abort(404)
    return jsonify(character.serialize())

@app.route('/character', methods=['POST'])
def add_character():
    data = request.json
    name = data['name']
    newCharacter = Character(name=name)
    db.session.add(newCharacter)
    db.session.commit()
    return jsonify(newCharacter.serialize()), 201

@app.route('/character/<string:character_id>', methods=['PUT'])
def update_character(character_id):
    selectCharacter = Character.query.get(character_id)
    if selectCharacter is None:
        abort(404)
    selectCharacter.name = request.json['name']
    db.session.commit()
    return jsonify(selectCharacter.serialize())

@app.route('/character/<string:character_id>', methods=['DELETE'])
def delete_character(character_id):
    selectCharacter = Character.query.get(character_id)
    if selectCharacter is None:
        abort(404)
    db.session.delete(selectCharacter)
    db.session.commit()
    return jsonify({'result': 'Success deleting'})


################# PLANETS ###################

@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets])

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        abort(404)
    return jsonify(planet.serialize())

@app.route('/planet', methods=['POST'])
def add_planet():
    data = request.json
    name = data['name']
    newPlanet = Planet(name=name)
    db.session.add(newPlanet)
    db.session.commit()
    return jsonify(newPlanet.serialize()), 201

@app.route('/planet/<string:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    selectPlanet = Planet.query.get(planet_id)
    if selectPlanet is None:
        abort(404)
    selectPlanet.name = request.json['name']
    db.session.commit()
    return jsonify(selectPlanet.serialize())

@app.route('/planet/<string:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    selectPlanet = Planet.query.get(planet_id)
    if selectPlanet is None:
        abort(404)
    db.session.delete(selectPlanet)
    db.session.commit()
    return jsonify({'result': 'Success deleting'})


################# STARSHIP ###################

@app.route('/starship', methods=['GET'])
def get_starships():
    starships = Starship.query.all()
    return jsonify([starship.serialize() for starship in starships])

@app.route('/starship/<int:starship_id>', methods=['GET'])
def get_single_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship is None:
        abort(404)
    return jsonify(starship.serialize())

@app.route('/starship', methods=['POST'])
def add_starship():
    data = request.json
    name = data['name']
    newStarship = Starship(name=name)
    db.session.add(newStarship)
    db.session.commit()
    return jsonify(newStarship.serialize()), 201

@app.route('/starship/<string:starship_id>', methods=['PUT'])
def update_starship(starship_id):
    selectStarship = Starship.query.get(starship_id)
    if selectStarship is None:
        abort(404)
    selectStarship.name = request.json['name']
    db.session.commit()
    return jsonify(selectStarship.serialize())

@app.route('/starship/<string:starship_id>', methods=['DELETE'])
def delete_starship(starship_id):
    selectStarship = Starship.query.get(starship_id)
    if selectStarship is None:
        abort(404)
    db.session.delete(selectStarship)
    db.session.commit()
    return jsonify({'result': 'Success deleting'})


################# FAVORITES ##################

@app.route('/user/<string:user_id>/favorites', methods=['GET'])
def get_favorite_from_user(user_id):
    user = User.query.get(user_id) 
    if user is None:
        abort(404) 

    favorites = []
    for character in user.characters:
        favorites.append({
            "type": "character",
            "id": character.id,
            "name": character.name
        })

    for planet in user.planets:
        favorites.append({
            "type": "planet",
            "id": planet.id,
            "name": planet.name
        })

    return jsonify(favorites)


@app.route('/user/<string:user_id>/favorites/ch', methods=['POST'])
def add_favorite_ch_to_user(user_id):
    user = User.query.get(user_id)  
    if user is None:
        abort(404) 

    data = request.json
    character_id = data.get('character_id')

    character = Character.query.get(character_id)  
    if character is None:
        abort(404)  

    user.characters.append(character)
    db.session.commit()

    return jsonify(user.serialize())



@app.route('/user/<string:user_id>/favorites/pl', methods = ['POST'])
def add_favorite_pl_to_user(user_id):
    user = User.query.get(user_id)  
    if user is None:
        abort(404) 

    data = request.json
    planet_id = data.get('planet_id')

    planet = Planet.query.get(planet_id)
    if planet is None:
        abort(404)
    user.planets.append(planet)
    db.session.commit()

    return jsonify(user.serialize())










# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
