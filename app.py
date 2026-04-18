from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from models import db
from routes import create_blueprints
from config import config
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config[config_name])

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)

    blueprints = create_blueprints()
    for bp in blueprints:
        app.register_blueprint(bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200

    @app.route('/sitemap.xml')
    def sitemap():
        static_dir = app.static_folder or 'static'
        return send_from_directory(static_dir, 'sitemap.xml', mimetype='application/xml')

    @app.route('/robots.txt')
    def robots():
        static_dir = app.static_folder or 'static'
        return send_from_directory(static_dir, 'robots.txt', mimetype='text/plain')

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

    return app

def init_db(app):
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    app = create_app()
    init_db(app)
    app.run(debug=True, host='0.0.0.0', port=5000)

app = create_app()
