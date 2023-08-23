#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_dict = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(bakeries_dict), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery_search = Bakery.query.filter_by(id=id).first()
    bakery_id = bakery_search.to_dict()
    return make_response(jsonify(bakery_id), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    price_array = [price.to_dict() for price in baked_goods_price]
    return make_response(jsonify(price_array), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    expensive_baked_good = baked_goods.to_dict()
    return make_response(jsonify(expensive_baked_good), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
