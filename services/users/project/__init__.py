import os
from flask import Flask
# , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app(script_info=None):
    # instanciando la app
    app = Flask(__name__)

    # enable CORS
    CORS(app)  # nuevo

    # estableciendo configuración
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # configurando extensiones
    db.init_app(app)

    # registrando blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # contexto shell para flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
