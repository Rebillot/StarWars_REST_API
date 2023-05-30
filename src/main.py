from flask import Flask, request, jsonify, abort
from models import Character, Planet, Starships
from app import app, db


@app.route("/<data_type>", method=["GET"])
def provide_data(data_type):
    if data_type == "Character":
        charactersData = db.query.all()
        return jsonify([character.serialize() for character in charactersData])
    elif data_type == "Planet":
        planetsData = db.query.all()
        return jsonify([planet.serialize() for planet in planetsData])
    elif data_type == "Starships":
        starshipsData = db.query.all()
        return jsonify([starship.serialize() for starship in starshipsData])
    else:
        return jsonify("Error: data type not correcto")


@app.route("/character/<string:id>", method=["GET"])
def provide_id(id):
    id = Character.query.get(id)
    if id is None:
        abort(404)
    return jsonify(Character.serialize())

@app.route("/planet/<string:id>", method=["GET"])
def provide_id(id):
    id = Planet.query.get(id)
    if id is None:
        abort(404)
    return jsonify(Planet.serialize())

@app.route("/starships/<string:id>", method=["GET"])
def provide_id(id):
    id = Starships.query.get(id)
    if id is None:
        abort(404)
    return jsonify(Starships.serialize())








# @app.route('/Character', methods=['GET'])
# def get_Characters():
#     charactersData = db.query.all()
#     return jsonify([character.serialize() for character in charactersData])


# @app.route('/Planet', methods=['GET'])
# def get_Planets():
#     planetsData = db.query.all()
#     return jsonify([planet.serialize() for planet in planetsData])


# @app.route('/Starships', methods=['GET'])
# def get_Starships():
#     starshipsData = db.query.all()
#     return jsonify([starship.serialize() for starship in starshipsData])
