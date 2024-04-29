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
from models import db, User, People, Planets, Favorites
#from models import Person

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

    users= User.query.all()
    all_users= list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

@app.route('/people', methods=['GET'])
def get_all_people():

    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))

    return jsonify(all_people), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):

    people = People.query.get(people_id)
    if people is None:
        return "No People with id: " + str(people_id), 400
    
    one_people = people.serialize()

    return jsonify(one_people), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_planets), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets(planet_id):

    planets = Planets.query.get(planet_id)
    if planets is None:
        return "No Planet with id: " + str(planet_id), 400
    
    one_planet = planets.serialize()

    return jsonify(one_planet), 200

@app.route('/user/favorites', methods=['GET'])
def get_favorites():

    favorites = Favorites.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))
    print(all_favorites)
    return jsonify(all_favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def new_favorite_planet(planet_id):
 

    new_fav = Favorites(
        userId = 1,
        planetId = planet_id,
        peopleId = None
    )
    
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"msg": "New Favorite is Created"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def new_favorite_people(people_id):

 
    new_fav = Favorites(
        userId = 1,
        planetId = None,
        peopleId = people_id
    )
    
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"msg": "New Favorite is Created"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):

    fav= []
    favorites = Favorites.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))
    for item in all_favorites:
        if item["planetId"] == planet_id:
           fav = item["id"]
    
    delete_fav_planet= Favorites.query.get(fav)
    db.session.delete(delete_fav_planet)
    db.session.commit()

   

    return jsonify({"msg" : "Favorite deleted"})

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(people_id):

    fav= []
    favorites = Favorites.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))
    for item in all_favorites:
        if item["peopleId"] == people_id:
           fav = item["id"]
    
    delete_fav_planet= Favorites.query.get(fav)
    db.session.delete(delete_fav_planet)
    db.session.commit()

   

    return jsonify({"msg" : "Favorite deleted"})
    


@app.route('/people', methods=['POST'])
def create_people():

    new_people = request.get_json()

    if 'name' not in new_people:
        return "Name should be in New People Body", 400
    

    new_people = People(
        name = new_people['name'], 
        age = new_people['age'],
        gender = new_people['gender']
    )

    db.session.add(new_people)
    db.session.commit()

    return jsonify({"msg": "New People is Created"}), 201


@app.route('/people/<int:people_id>', methods=['PUT'])
def update_people(people_id):

    new_updated_people = request.get_json()
    old_people_obj = People.query.get(people_id)

    if old_people_obj is None:
        return "No People with id: " + str(people_id), 400

    if 'name' in new_updated_people:
        old_people_obj.name = new_updated_people['name']

    if 'age' in new_updated_people:
        old_people_obj.age = new_updated_people['age']

    if 'gender' in new_updated_people:
        old_people_obj.gender = new_updated_people['gender']

    db.session.commit()

    return jsonify({"msg": "Peeple is Updated"}), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):

    deleting_people = People.query.get(people_id)

    if deleting_people is None:
        return "No People with id: " + str(people_id), 400

    db.session.delete(deleting_people)
    db.session.commit()

    return jsonify({"msg": "People is Deleted"}), 200




@app.route('/planet', methods=['POST'])
def create_planet():

    new_planet = request.get_json()

    if 'name' not in new_planet:
        return "Name should be in New Planet Body", 400
    

    new_planet = Planets(
        name = new_planet['name'], 
        size = new_planet['size'],
        climate = new_planet['climate']
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "New Planet is Created"}), 201



@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):

    new_updated_planet = request.get_json()
    old_planet_obj = Planets.query.get(planet_id)

    if old_planet_obj is None:
        return "No People with id: " + str(planet_id), 400

    if 'name' in new_updated_planet:
        old_planet_obj.name = new_updated_planet['name']

    if 'age' in new_updated_planet:
        old_planet_obj.size = new_updated_planet['size']

    if 'gender' in new_updated_planet:
        old_planet_obj.climate = new_updated_planet['climate']

    db.session.commit()

    return jsonify({"msg": "Planet is Updated"}), 200


@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    deleting_planet = Planets.query.get(planet_id)

    if deleting_planet is None:
        return "No People with id: " + str(planet_id), 400

    db.session.delete(deleting_planet)
    db.session.commit()

    return jsonify({"msg": "Planet is Deleted"}), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
