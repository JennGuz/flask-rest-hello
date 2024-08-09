"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
# from models import Person

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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/users', methods=['GET'])
def get_users():
    
    users = db.session.execute(db.select(User)).scalars()

    user_list = [user.serialize() for user in users]

    return jsonify(user_list), 200


@app.route('/people', methods=['GET'])
def get_people():
    all_characters = db.session.execute(db.select(Character)).scalars()

    character_list = [character.serialize() for character in all_characters]

    return jsonify(character_list), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = db.get_or_404(Character, people_id)
    
    return jsonify(character.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = db.session.execute(db.select(Planet)).scalars()

    planet_list = [planet.serialize() for planet in all_planets]

    return jsonify(planet_list), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = db.get_or_404(Planet, planet_id)
    
    return jsonify(planet.serialize()), 200


@app.route('/users/favorites', methods=['GET'])
def get_favorites():

    user_id = request.args.get('user_id')

    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400 
    
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "user_id must be an integer"}), 400
    
    favorites = db.session.execute(db.select(Favorite).filter(Favorite.user_id == user_id)).scalars()

    favorite_list = [favorite.serialize() for favorite in favorites]

    return jsonify(favorite_list), 200


@app.route('/add_favorite_planet', methods=['POST'])
def add_favorite_planet():

    user_id = get_current_user_id() 
    planet_id = request.json.get('planet_id')

    if not planet_id:
        return jsonify({"error": "planet_id is required"}), 400

    new_favorite = Favorite(user_id=user_id, favorite_id=planet_id, favorite_type='planet')

    db.session.add(new_favorite)
    db.session.commit() 

    return jsonify({"message": "Planet added to favorites successfully!"}), 201



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
