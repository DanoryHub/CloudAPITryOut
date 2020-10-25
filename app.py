from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

from db_config import db_url_getter
from models import db, Items

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url_getter.get_postgres_url()
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()


#Resources
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
    )
    parser.add_argument(
        'name',
        type=str,
        required=True
    )
        
    def get(self, _id):
        item = Items.query.filter_by(_id=_id).one()
        return {
            'item': 
                {
                    '_id': item._id,
                    'name': item.name,
                    'price': item.price
                }
            }
    
    def post(self, _id):
        if Items.query.filter_by(_id=_id).one_or_none() is not None:
            return {'message': f"Item with id '{_id}' already exists"}, 400
        
        data = Item.parser.parse_args()
        
        item = Items(name=data['name'], price=data['price'])

        db.session.add(item)
        db.session.commit()


        return {
            '_id': item._id,
            'name': item.name,
            'price': item.price 
            } 
    
    def delete(self, _id):
        Items.query.filter_by(_id=_id).delete()
        db.session.commit()
        return {'message': 'Item deleted'}
    
    def put(self, _id):
        data = Item.parser.parse_args()

        item = Items.query.filter_by(_id=_id).one_or_none()
        if not item:
            item = Items(name=data['name'], price=data['price'])
            db.session.add(item)
        else:
            Items.query.filter_by(_id=_id).update({'name': data['name'], 'price': data['price']})
        db.session.commit()
        return {
            '_id': item._id,
            'name': item.name,
            'price': item.price
        }


class ItemList(Resource):
    def get(self):
        items = Items.query.all()
        bunch_of_items = {
            'items':[]
        }
        for item in items:
            item_dict = {
                '_id': item._id,
                'name': item.name,
                'price': item.price
            }
            bunch_of_items['items'].append(item_dict)
        return bunch_of_items
# Endpoints 
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<int:_id>')

app.run(port=8000, host="0.0.0.0", debug=True)