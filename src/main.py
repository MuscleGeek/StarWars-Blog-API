"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json, flash
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap                                                            #raise APIExceptions
from admin import setup_admin
from models import db, User, People, Planet, Favorites                                                      #Class Tables from Models.py
import json
from werkzeug.security import generate_password_hash, check_password_hash                                   #WSGI Encrypter
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity              #JTW management



app = Flask(__name__)
app.url_map.strict_slashes = False
            # SETS UP the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "$$2021$$jvm@@"        # Change this "super secret" with something else!
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#region USER CRUD here...
@app.route('/user', methods=['GET'])                    #C"R"UD All Users
def get_users():
    users = User.query.all()
    payload = list(map(lambda u: u.serialize(),users))
    # DUMMY DATA#dummy_ser = User(1,"roflmao","male","lol@lol.com")
    # return jsonify(usuario.__repr__()), 200
    return jsonify(payload),200
# this only runs if `$ python src/main.py` is executed
@app.route('/user/<int:fid>', methods=['GET'])
def get_user_by_id(fid):
    user = User.query.filter_by(id=fid).first_or_404()
    return jsonify(user.serialize()), 200

@app.route('/user', methods=['POST'])                   #"C"RUD a new User              
def add_user():
    req_body = json.loads(request.data)
    if req_body["name"] == None and req_body["gender"] == None and req_body["password"] == None and req_body["email"] == None:
        return "Invalid data or empty slots"
    else:
        usr = User(name= req_body["name"], gender= req_body["gender"], password= req_body["password"], email= req_body["email"])
        db.session.add(usr)    
        db.session.commit()
        return("Data has been added successfully")

@app.route('/user/<int:fid>', methods=['DELETE'])
def del_user_by_id(fid):
    user = User.query.filter_by(id=fid).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return("User has been deleted successfully"), 200
#endregion USER CRUD here...

#region PEOPLE CRUD here
@app.route('/people', methods=['POST'])                   #"C"RUD People
def add_people():
    # add a character
    # DUMMY DATA#people = People(name='John',hair_color='Brown', skin_color='Black', height=1) 
    req_body = json.loads(request.data)  #Getting request data via json format to bridge FE-BE 
    
    #People data validation slots
    if req_body["name"] == None and req_body["hair_color"] == None and req_body["skin_color"] == None and req_body["height"] == None and req_body["birth_year"] == None and req_body["gender"] == None and req_body["image"] == None: #Validation slots => BD <= <&1...While every1 gets OK => it gets ahead then
        return "Invalid data or empty slots"
    else:
        ppl = People(name= req_body["name"], hair_color= req_body["hair_color"], skin_color= req_body["skin_color"], height= req_body["height"], birth_year= req_body["birth_year"], gender= req_body["gender"], image= req_body["image"]) #While all slots has been verified against None it's getting added to table and finally get commit by db.session
        db.session.add(ppl)   #applying new data entry
        db.session.commit()   #commit changes to db
        return "Data has been addded successfully"

@app.route('/people', methods=['GET'])                      #C"R"UD All People
def get_people():

    ppl = People.query.all()                                #it gets all data  by query method.. from ppl table
    payload = list(map(lambda p: p.serialize(),ppl))        #scan all data from table... at same it is being serialized
    return jsonify(payload), 200                            #Return the payload data via json type format to FE

@app.route('/people/<int:fid>', methods=['GET'])
def get_people_by_id(fid):

    ppl = People.query.filter_by(id=fid).first_or_404()
        #alternatives#
    #ppl = db.session.query(People).filter(People.id).first()
    #ppl= People.query.filter_by(id=id).first() 
    #ppl = session.query(People).get(id=id).first()
        #alternatives#
    return jsonify(ppl.serialize()), 200

@app.route('/people/<int:fid>', methods=['DELETE'])         #CRU"D" People by ID
def del_people_by_id(fid):

    ppl = People.query.filter_by(id=fid).first_or_404()
    db.session.delete(ppl)
    db.session.commit()
    return "Data has been deleted successfully"
#endregion People CRUD

#region PLANET CRUD  here...
@app.route('/planet', methods=['GET'])                      #C"R"UD All Planets
def get_planets():

    planet = Planet.query.all()
    payload = list(map(lambda w: w.serialize(),planet))
    return jsonify(payload), 200                            #same logic like above

@app.route('/planet', methods=['POST'])                     #"C"RUD Planet
def add_planet():
    # dummy data planet  = Planet(name='Marduk',hair_color='Brown',skin_color='Caucasian',height=2)
    req_body =  json.loads(request.data)                    #parsing json data to py dictionary
    if  req_body["name"] == None and req_body["diameter"] == None and req_body["climate"] == None and req_body["terrain"] == None and req_body["population"] == None and req_body["image"] == None: #Validation slots, if is get empty, null or undefined it is not getting valid 
        return "Los datos son invalidos o incompletos" 
    else:
        planet = Planet(name= req_body["name"], diameter= req_body["diameter"], climate= req_body["climate"], terrain= req_body["terrain"], population= req_body["population"], image= req_body["image"]) #While all slots got validated.. it is getting ok status
        db.session.add(planet)                              #applying new data into db (planet)
        db.session.commit()                                 #commit changes into db by session 
        return "Los datos han sido ingresados correctamente"

@app.route('/planet/<int:fid>', methods=['GET'])        #
def get_planet_by_id(fid):
    planet = Planet.query.filter_by(id=fid).first_or_404()  #Getting and matching ids or throwing 404 status code
    return jsonify(planet.serialize()), 200                 #return the object via json serialized format to FE

@app.route('/planet/<int:fid>', methods=['PUT'])            #CR"U"D Planet by ID
def update_planet(fid):
    planet = Planet.query.filter_by(id=fid).first_or_404()
    if planet == None:
        raise APIException("Planet not found", status_code=404)
                                                            
    req_body = json.load(request.data)
    if req_body["name"] == None and req_body["diameter"] == None and req_body["climate"] == None and req_body["terrain"] == None and req_body["population"] == None and req_body["image"] == None:
        flash("Planet has not been found")
    else:
        planet = Planet(name= req_body["name"], diameter= req_body["diameter"], climate= req_body["climate"], terrain= req_body["terrain"], population= req_body["population"], image=["image"])
        db.session.add(planet)
        db.session.commit()
        return "Planet has been updated successfully"
#endregion Planet CRUD

#region Favorites
@app.route('/favorites', methods=['GET'])                    #C"R"UD All Favorites                                                             
def get_favz():
    favz = Favorites.query.all()
    payload = list(map(lambda f: f.serialize(), favz))
    return jsonify(payload)

@app.route('/favorites/<int:fid>', methods=['GET'])          #C"R"UD Favorites by ID
def get_one_fav(fid):
    fav = Favorites.query.filter_by(id=fid).first_or_404()
    return jsonify(fav.serialize())

@app.route('/favorites', methods=['POST'])                   #"C"RUD Favorites
def add_new_fav():
    req_body = json.loads(request.data)
    if req_body["name"] == None and req_body["type"] == None:
        flash('Datos invalidos o campos incompletos')
    else:
        favs = Favorites(name=req_body["name"], type=req_body["type"])
        db.session.add(favs)
        db.session.commit()
        return "Data has been added successfully"

@app.route('/favorites/<int:fid>', methods=['PUT'])            #CR"U"D Favorites by ID
def update_fav(fid):
    fav = Favorites.query.filter_by(id=fid).first_or_404()
    if fav == None:
        raise APIException("Favorite has not been found", status_code=404)

    req_body = json.loads(request.data)
    if req_body["name"] == None and req_body["type"] == None:
        flash("Campos incompletos o invalidos")
    else:
        favs = Favorites(name= req_body["name"], type= req_body["type"])
        db.session.add(favs)
        db.session.commit()
        return "Favorite has been updated successfully"

@app.route('/favorites/<int:fid>', methods=["DELETE"])          #CRU"D" by Favorites ID
def del_one_fav(fid):
    favz = People.query.filter_by(id=fid).first_or_404()
    db.session.delete(favz)
    db.session.commit()
    return('Favorite has been deleted successfully')  
#endregion Favorites

#region Registration
@app.route('/signup', methods=["POST"])
def signup():
    if request.method == 'POST':
        name= request.json.get("name", None)
        gender = request.json.get("gender", None)
        password = request.json.get("password", None)
        email = request.json.get("email", None)
                                                                #BEGIN Validation Block
        if not email:
            return jsonify({"msg:" "nombre es requerido"}), 400
        if not gender:
            return jsonify({"msg:" "genero es requerido"}), 400
        if not password:
            return jsonify({"msg:" "password es requerido"}), 400
        if not email:
            return jsonify({"msg:" "email es requerido"}), 400
        
        signup = User.query.filter_by(email = email).first_or_404()
        if signup:
                return jsonify({"msg": "Username already exists"}), 400
                                                                #END Validation Block
        signup = User()                                         #User table instance
        signup.name = name
        signup.gender = gender                                    #email attr
        sha256encode =generate_password_hash(password)          #generating hash via sha265 cryptography to password
        print(len(sha256encode))
        signup.password = sha256encode                            #cryptographically password hashed via sha256. Althrough, sha512 is an option too
        print(len(user.password))
        signup.email = email
        db.session.add(signup)                                  #added into db
        db.session.commit()                                     #commit changes

        return jsonify({"sucess": "Account has been created successfully", "status": "true"}), 200
#endRegion Registration

#region Auth Login
@app.route('/signin', methods=['POST'])                         #Log In route for Login Form
def get_logged_in():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg:" "User is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400
        
        usr = User.query.filter_by(email=email).first_or_404()
        if not usr:
            return jsonify({"msg": "User/email not valid"}), 401

        if not check_password_hash(usr.password, password):
            return jsonify({"msg": "User/Password not valid"}), 401 

    #region Token Built
        expiring_token = datetime.timedelta(days=1)              #token expires ~1 day
        accesing_token = create_access_token(identity=usr.email, expires_delta=expires_delta)  #we would be able to access via token using email and it checks by delta
        data = {"user": usr.serialize(), "access":access_token, "expires": expiring_token.total_seconds()*1000} #set token to data object

        return jsonify(data), 200    
    #endregion Token Built    
#endregion Auth Login

#region Profile Acc
@app.route('/profile', methods=['GET'])                         #getting profile dashboard after having gotten token validation by jwt_identity active session
@jwt_required()
def profile():
    if request.method == 'GET':
        token = get_jwt_identity()
        return({"success": "Access to private Profile", "user":token}), 200
#endregion Profile Acc

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))                    #default port for os=>env
    app.run(host='0.0.0.0', port=PORT, debug=True)             #running 127.0.0.1 and debug feature turned off
