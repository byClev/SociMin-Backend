from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from app.auth import bp as auth_bp
    from app.storage import bp as storage_bp
    from app.blog import bp as blog_bp
    from app.forum import bp as forum_bp

    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(storage_bp)
    app.register_blueprint(forum_bp)

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app
