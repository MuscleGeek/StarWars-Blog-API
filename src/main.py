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
from models import db, User, People, Planet, Favorites
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
    # usuario = User(1,"roflmao","male","lol@lol.com")
    # return jsonify(usuario.__repr__()), 200
    return jsonify(response_body),200
# this only runs if `$ python src/main.py` is executed

@app.route('/people', methods=['POST'])
def add_people():
    # add a character
    #people = People(name='John',hair_color='Brown', skin_color='Black', height=1) 
    request_body = json.loads(request.data)
    #people data validation
    if request_body["name"] == None and request_body["hair_color"] == None and request_body["skin_color"] == None and request_body["height"]:
        return "Los datos son incompletos o invalidos"
    else:
        ppl = People(name= request_body.name, hair_color= request.hair_color, skin_color= request.skin_color, height= request_body.height)
    db.session.add(ppl)
    db.session.commit()
    return "Post exitoso"

@app.route('/people', methods=['GET'])
def get_people():
    ppl = People.query.all()
    resultado = list(map(lambda x: x.serialize(),ppl))
    return jsonify(resultado)

@app.route('/planet', methods=['GET'])
def get_planet():
    planet = Planet.query.all()
    resultado = list(map(lambda x: x.serialize(),planet))
    return jsonify(resultado)

@app.route('/planet', methods=['POST'])
def add_planet():
    # dummy data planet  = Planet(name='Marduk',hair_color='Brown',skin_color='Caucasian',height=2)
    request_body =  json.loads(request.data)
    if request_body["name"] == None and request_body["diameter"] == None and request.data["climate"] == None and request.data["terrain"] and request.data["population"]:
        return "Los datos son invalidos o incompletos" 
    else:
        planet = Planet(name= request_body.name, diameter= request_data.diameter, climate= request_body.climate, terrain= request_body.terrain, population= request_body.population)
    db.session.add(planet)
    db.session.commit()
    return "Los datos han sido ingresados correctamente"


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
