from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):  # define resource

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name} already exists."}, 400

        data = Item.parser.parse_args()  # parse_args() parses thru the JSON payload and puts valid ones into data variable
        item = ItemModel(name, data['price'], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting the item."}, 500  # internal server error
                                                                              # not requester's fault, the server messed up
        return item.json(), 201  # we have to always return JSON format, not item object

    def put(self, name):
        data = Item.parser.parse_args()  # parse_args() parses thru the JSON payload and puts valid ones into data variable

        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data["store_id"]

        item.save_to_db()

        return item.json()


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


class ItemList(Resource):

    def get(self):
        return {'items': [i.json() for i in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}   # this works as well