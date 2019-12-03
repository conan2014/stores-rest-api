from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()   # SQLAlchemy only creates tables that it sees according to import
                      # So if we delete 'from resources.store import Store, StoreList', then SQLAlchemy won't create stores table