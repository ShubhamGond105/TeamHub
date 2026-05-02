import os
import sys

# Ensure Vercel can import from the backend directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config
from models import db


def create_app():
    # Use absolute paths so Vercel can find the frontend folder from the root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(base_dir, 'frontend')
    app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.projects import projects_bp
    from routes.members import members_bp
    from routes.tasks import tasks_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(members_bp, url_prefix='/api')
    app.register_blueprint(tasks_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')

    # Serve frontend
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        try:
            return send_from_directory(app.static_folder, path)
        except Exception:
            return send_from_directory(app.static_folder, 'index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        if request_wants_json():
            return jsonify({'error': 'Not found'}), 404
        return send_from_directory(app.static_folder, 'index.html')

    with app.app_context():
        db.create_all()

    return app


def request_wants_json():
    from flask import request
    return (
        request.path.startswith('/api/') or
        request.accept_mimetypes.best == 'application/json'
    )


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
