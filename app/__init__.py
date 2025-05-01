from flask import Flask, render_template
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Replace with a secure random key in production

    baseDir = os.path.abspath(os.path.dirname(__file__)) 
    dbPath = os.path.join(baseDir, 'data', 'app.db')
    app.config['DATABASE'] = dbPath
    
    #import blueprints
    from app.Boundaries.Login import auth_bp
    from app.Boundaries.Admin import admin_bp
    from app.Boundaries.LayoutPartials import layout_bp

    #register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(layout_bp, url_prefix='/partials')

    @app.route('/')
    def index():
        return render_template('LoginPage/login.html')

    return app
