import os

# app.py konfiguracijos failas

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/events.db'


class HerokuConfig(BaseConfig):
    # postgres duombazė heroku aplinkoj
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
