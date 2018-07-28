from flask_restful import Resource, reqparse
from flask_jwt import JWT,jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                type = float,
                required = True,
                help = 'This field cannot be left blank!'
            )

    parser.add_argument('store_id',
                type = int,
                required = True,
                help = 'Every item needs a store id!'
            )
    @jwt_required() # этот декоратор требует аутентификацию перед выполнением ф-ции
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items),None)
        # return {'item' : item}, 200 if item else 404
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'msg' : 'item not found'}

    def post(self,name):
        if ItemModel.find_by_name(name):
        #if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'msg': 'An item with name {} already exists'.format(name)}, 400 # bad request

        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'], request_data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'msg' : 'An error occured inserting the item.'}, 500 # Internal Server Error

        return item.json(), 201 #created

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'msg':'item deleted'}

    def put(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        #updated_item = {'name':name, 'price': request_data['price']}
        #updated_item = ItemModel(name,request_data['price'])

        if item is None:
            item = ItemModel(name, request_data['price'], request_data['store_id'])
        else:
            item.price = request_data['price']
            item.store_id = request_data['store_id']

        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # or return {'items':list(map(lambda x: x.json(), ItemModel.query.all()))}
