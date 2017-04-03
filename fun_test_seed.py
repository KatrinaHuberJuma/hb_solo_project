from model import connect_to_db, db
from tests import create_pair
from server import app

safe_to_proceed = raw_input("did you drop katfuntest since the last time you ran this? did your recreate it? (y/n)")

if safe_to_proceed == 'y':
    connect_to_db(app, "postgresql:///katfuntest")
    db.create_all()

    create_pair()