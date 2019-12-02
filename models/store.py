from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # Back reference
    # It allows a store to see which items are in the item database, or in the items table
    # with the store_id equal to its own id
    # The way we do that is as follows:
    items = db.relationship("ItemModel", lazy='dynamic') # this line allows SQLAlchemy to retrieve an ItemModel object
                                                         # with store_id matching the id property
                                                         # defined in the StoreModel here

                                                         # If we don't set lazy='dynamic', then each time we create a store we load up
                                                         # all the items in memory, and then we can call .json() method many times for free

                                                         # set lazy='dynamic', self.items is no longer a list of item objects
                                                         # self.items becomes a query that we can run
                                                         # Essentially, related items are not loaded each time when a Store object is created.
                                                         # This makes creating a store quicker, but in exchange it will be a bit slower when
                                                         # you want to actually access the items
                                                         # which means unless .json() is called, we are not looking into items table
                                                         # When .json() is called, we have to go into the table, so it's gonna be slower

                                                         # so there is a trade-off between speed of creation of the store and
                                                         # speed of calling .json() method

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


