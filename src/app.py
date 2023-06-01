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
from models import db, User, Character


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

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])


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





# @app.route("/character/<string:id>", method=["GET"])
# def provide_id(id):
#     id = Character.query.get(id)
#     if id is None:
#         abort(404)
#     return jsonify(Character.serialize())

# @app.route("/planet/<string:id>", method=["GET"])
# def provide_id(id):
#     id = Planet.query.get(id)
#     if id is None:
#         abort(404)
#     return jsonify(Planet.serialize())

# @app.route("/starships/<string:id>", method=["GET"])
# def provide_id(id):
#     id = Starships.query.get(id)
#     if id is None:
#         abort(404)
#     return jsonify(Starships.serialize())










# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
