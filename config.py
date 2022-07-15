from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = 'make this more secret'
    FLASK_SECRET = SECRET_KEY
    DB_HOST = 'database' # do this later

class DebugConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DB_HOST = 'my.production.database' 

