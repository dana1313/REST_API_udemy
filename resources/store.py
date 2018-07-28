from flask_restful import Resource, reqparse
from flask_jwt import JWT,jwt_required
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {'msg':'store was not found'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'msg': 'store {} already exists'.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'msg': 'An error occurred while creating the store'}, 500

        return store.json(), 201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {'msg':"An error occurred while deleting store"}, 500

        return {'msg':'store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}