import os

from flask import Flask

from routes.site import bp as site_bp

from database import db


def create_app():
    """sukuria puslapį naudojant Flask"""
    app = Flask(__name__)

    # konfiguracija iš config.py failo
    app.config.from_object(os.getenv('FLASK_CONFIG', 'config.DevConfig'))

    # registruoja blueprint
    app.register_blueprint(site_bp)
    
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
