#!/usr/bin/env python3
import os
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Restaurant, Pizza, RestaurantPizza

api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class RestaurantListResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants])

    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or 'address' not in data:
            return make_response(jsonify({"error": "Incomplete data"}), 400)

        new_restaurant = Restaurant(
            name=data['name'],
            address=data['address']
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return make_response(jsonify(new_restaurant.to_dict()), 201)

class RestaurantResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)
        
        restaurant_dict = restaurant.to_dict()
        restaurant_dict['restaurant_pizzas'] = [rp.to_dict() for rp in restaurant.pizzas]
        return jsonify(restaurant_dict)

    def patch(self, id):
        data = request.get_json()
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)
        
        if 'name' in data:
            restaurant.name = data['name']
        if 'address' in data:
            restaurant.address = data['address']
        
        db.session.commit()
        return make_response(jsonify(restaurant.to_dict()), 200)

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)
        
        db.session.delete(restaurant)
        db.session.commit()
        return make_response('', 204)

class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict() for pizza in pizzas])

    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or 'ingredients' not in data:
            return make_response(jsonify({"error": "Incomplete data"}), 400)
        
        new_pizza = Pizza(
            name=data['name'],
            ingredients=data['ingredients']
        )
        db.session.add(new_pizza)
        db.session.commit()
        return make_response(jsonify(new_pizza.to_dict()), 201)

class PizzaResource(Resource):
    def get(self, id):
        pizza = Pizza.query.get(id)
        if not pizza:
            return make_response(jsonify({"error": "Pizza not found"}), 404)
        
        return jsonify(pizza.to_dict())

    def patch(self, id):
        data = request.get_json()
        pizza = Pizza.query.get(id)
        if not pizza:
            return make_response(jsonify({"error": "Pizza not found"}), 404)
        
        if 'name' in data:
            pizza.name = data['name']
        if 'ingredients' in data:
            pizza.ingredients = data['ingredients']
        
        db.session.commit()
        return make_response(jsonify(pizza.to_dict()), 200)

    def delete(self, id):
        pizza = Pizza.query.get(id)
        if not pizza:
            return make_response(jsonify({"error": "Pizza not found"}), 404)
        
        db.session.delete(pizza)
        db.session.commit()
        return make_response('', 204)

class RestaurantPizzaResource(Resource):
    def post(self):
        data = request.get_json()

        required_fields = ['price', 'restaurant_id', 'pizza_id']
        if not data or not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Incomplete data"}), 400)

        if not (1 <= data['price'] <= 30):
            return make_response(jsonify({"error": "Price must be between 1 and 30"}), 400)

        restaurant = Restaurant.query.get(data['restaurant_id'])
        pizza = Pizza.query.get(data['pizza_id'])

        if not restaurant:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)
        if not pizza:
            return make_response(jsonify({"erro


