# Flask Application Entrypoint

# OS Functions
import os
from os import environ
from os.path import dirname, exists, join

# Flask
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from config import config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
admin = Admin(name='MyApp', template_mode='bootstrap3')


def createApp(configName):
    app = Flask(__name__)
    app.config.from_object(config[configName])
    config[configName].init_app(app)

    db.init_app(app)
    admin.init_app(app)

    from app.models import User
    admin.add_view(ModelView(User, db.session))

    csrf.init_app(app)
    login_manager.init_app(app)
    

    login_manager.login_view = '/login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.query(User).filter_by(id=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        app.logger.warning('User unauthorized : URL(%s)' % (request.url))
        # do stuff
        return redirect(url_for('users.login'))

    # Blueprints
    from app.blueprints.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    def format_datetime(value, format='human'):
        if format == 'human':
            format = '%B %d, %Y at %-I:%-M%p'
        return value.strftime(format)

    def format_date(value, format='human'):
        if format == 'human':
            format = '%B %d, %Y'
        return value.strftime(format)

    app.jinja_env.filters['format_datetime'] = format_datetime
    app.jinja_env.filters['format_date'] = format_date

    CSRF Error Handler
    from flask_wtf.csrf import CSRFError
    from flask import abort, flash

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        app.logger.warning('CSRF error : %r' % e)
        flash('CSRF Error. Please go back, refresh the page and try again.', 'warning')
        return abort(405)

    return app
