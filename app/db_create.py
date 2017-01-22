from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO
import os.path
db.create_all()