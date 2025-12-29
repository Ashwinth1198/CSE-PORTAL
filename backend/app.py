from flask import Flask, redirect, url_for, render_template
from config import Config
from extensions import db
from flask_login import LoginManager
from models.user_model import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from routes.auth_routes import auth
    from routes.admin_routes import admin
    from routes.student_routes import student

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(student)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @app.route('/favicon.ico')
    def favicon():
        return redirect(url_for('static', filename='favicon.ico'))

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
