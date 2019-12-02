from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):  # define resource

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"A store with name {name} already exists."}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': "An error occurred while creating the store."}, 500  # internal server error
                                                                                    # not requester's fault, the server messed up
        return store.json(), 201  # we have to always return JSON format, not store object

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), StoreModel.query.all()))}   # this works as well