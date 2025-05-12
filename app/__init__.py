from flask import Flask, render_template
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Replace with a secure random key in production

    baseDir = os.path.abspath(os.path.dirname(__file__)) 
    dbPath = os.path.join(baseDir, 'data', 'app.db')
    app.config['DATABASE'] = dbPath
    
    #import blueprints
    from app.Boundaries.Auth import auth_bp
    from app.Boundaries.Admin import admin_bp
    from app.Boundaries.AdminAPI import admin_api_bp
    from app.Boundaries.Cleaner import cleaner_bp
    from app.Boundaries.CleanerAPI import cleaner_api_bp
    from app.Boundaries.LayoutPartials import layout_bp
    from app.Boundaries.HomeOwner import homeowner_bp
    from app.Boundaries.HomeOwnerAPI import homeowner_api_bp
    from app.Boundaries.PlatformManagement import platform_bp
    from app.Boundaries.PlatformManagementAPI import platform_api_bp

    #register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(admin_api_bp, url_prefix='/api/admin')
    app.register_blueprint(cleaner_bp, url_prefix='/cleaner')
    app.register_blueprint(cleaner_api_bp, url_prefix='/api/cleaner')
    app.register_blueprint(layout_bp, url_prefix='/partials')
    app.register_blueprint(homeowner_bp, url_prefix='/homeowner')
    app.register_blueprint(homeowner_api_bp, url_prefix='/api/homeowner')
    app.register_blueprint(platform_bp, url_prefix='/platform')
    app.register_blueprint(platform_api_bp, url_prefix='/api/platform')

    @app.route('/')
    def index():
        return render_template('LoginPage/login.html')
    
    # Add after_request handler to prevent caching of sensitive pages
    @app.after_request
    def no_cache(response):
        # Set headers to prevent browser from caching protected pages
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    return app
