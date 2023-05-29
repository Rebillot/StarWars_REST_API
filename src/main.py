from flask import Flask, request, jsonify, abort
from models import Character
from app import db


@app.route('/Character', methods=['GET'])
def get_Characters():
    charactersData = db.query.all()
    return jsonify(character.serialize() for character in charactersData)




