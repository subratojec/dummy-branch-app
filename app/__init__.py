from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config

# single shared SQLAlchemy instance for the app
db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    # initialize extensions
    db.init_app(app)

    # Lazy imports to avoid circular deps during app init
    from .routes.health import bp as health_bp
    from .routes.loans import bp as loans_bp
    from .routes.stats import bp as stats_bp

    # register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")

    return app
