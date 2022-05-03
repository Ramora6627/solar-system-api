from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request


# planet_bp = Blueprint("books", __name__, url_prefix = "/planets")

# class Planet:
#     def __init__(self, id, name, description, moons):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.moons = moons
#     def to_json(self):
#         return {
#                 "id": self.id,
#                 "name": self.name,
#                 "desciption": self.description,
#                 "moons": self.moons
#             }

# planets = [
#             Planet(1, "Mercury", "the nearest planet to the Sun", 0),
#             Planet(2, "Venus", "named after the Roman goddess of love and beauty", 0),
#             Planet(3, "Earth", "Home. the only astronomical object known to harbor life", 1),
#             Planet(4, "Mars", "is often called the Red Planet", 2),
#             Planet(5, "Jupiter", "more then 2.5 time the mass of all other planets", 79),
#             Planet(6, "Saturn", "second-largest planet in the Solar System", 82),
#             Planet(7, "Uranus", "named after the Greek god of the sky", 27),
#             Planet(8, "Neptune", "the densest giant planet", 14),
#             Planet(9, "Pluto", "may or may not be a planet, poor Pluto", 1)
#             ]
planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")
# Helper function:

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"planet {planet_id} invalid"}, 400))

    planet = Planet.query.get(planet_id)
    if not planet:
        abort(make_response({"message":f"planet {planet_id} not found"}, 404))
    return planet


@planet_bp.route("", methods=["POST"])
def create_planets():
    request_body = request.get_json()
    
    try:
        new_planet = Planet(name = request_body["name"], description = request_body["description"], moons = request_body["moons"])
        db.session.add(new_planet)
        db.session.commit()
    except:
        abort(make_response({"message":f"invalid input"}, 400))
    return make_response(f"Planet {new_planet.name} successfully created", 201)

@planet_bp.route("", methods=["GET"])
def read_all_planets():
    planets_response = []

    name_query = request.args.get("name")
    
    if name_query:
        planets = Planet.query.filter_by(name = name_query)
    else:
        planets = Planet.query.all()
        
    try:
        for planet in planets:
            planets_response.append(
                {
                    "id": planet.id,
                    "name": planet.name,
                    "description": planet.description,
                    "moons": planet.moons
                }
            )
    except:
        abort(make_response({"message":f"planet not found"}, 404))
    return jsonify(planets_response)




@planet_bp.route("/<planet_id>", methods=["GET"])
def read_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return jsonify(planet.to_json(), 200)

    # planets_response = []
    # for planet in planets:
    #     planets_response.append(planet.to_json())
    # return jsonify(planets_response), 200

@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_planet(planet_id)

    request_body = request.get_json()
    try: 
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.moons = request_body["moons"]
    except:
        abort(make_response({"message":f"invalid data"}, 400))
    
    db.session.commit()

    return jsonify(planet.to_json(), 200)

@planet_bp.route("/<planet_id>", methods=["DELETE"])
def delete_a_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response({"message":f"planet{planet_id} successfully deleted"}, 200)