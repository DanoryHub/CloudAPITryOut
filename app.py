from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

# "Database" :D
items = []

#Resources
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
    )
        
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}
    
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f"Item with name '{name}' already exists"}, 400
        
        data = Item.parser.parse_args()
        
        item = {
            'name': name, 
            'price': data['price']
            }

        items.append(item)
        return item 
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if not item:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}
# Endpoints 
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<string:name>')

app.run(port=8000, debug=True)