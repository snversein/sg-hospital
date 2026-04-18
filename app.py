from flask import Flask, render_template, jsonify, request, send_from_directory, Response
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
        sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://drsushmitaayurveda.in/</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/#about</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/#services</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/#testimonials</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/#contact</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/admin</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/admin/dashboard</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/admin/appointments</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/admin/messages</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/admin/patients</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://drsushmitaayurveda.in/api/contact</loc>
        <lastmod>2026-04-18</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.3</priority>
    </url>
</urlset>"""
        return Response(sitemap_xml, mimetype='application/xml')

    @app.route('/robots.txt')
    def robots():
        robots_txt = """User-agent: *
Allow: /

Sitemap: https://drsushmitaayurveda.in/sitemap.xml"""
        return Response(robots_txt, mimetype='text/plain')

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
