from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Replace with a secure random key in production

    #import blueprints
    from app.Boundaries.Login import auth_bp
    from app.Boundaries.Admin import admin_bp

    #register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route('/')
    def index():
        return render_template('login.html')

    return app
