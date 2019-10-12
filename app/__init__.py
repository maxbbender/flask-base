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

# from flask_mail import Mail, email_dispatched
# from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(name='MyApp', template_mode='bootstrap3')

# mail = Mail()
# csrf = CSRFProtect()


def createApp(configName):
    app = Flask(__name__)
    app.config.from_object(config[configName])
    config[configName].init_app(app)

    db.init_app(app)
    admin.init_app(app)

    from app.models import User
    admin.add_view(ModelView(User, db.session))

    # mail.init_app(app)
    # csrf.init_app(app)
    # login_manager.init_app(app)
    

    # login_manager.login_view = '/login'

    # @login_manager.user_loader
    # def load_user(user_id):
    #     from app.models.user import User
    #     return db.session.query(User).filter_by(id=user_id).first()

    # @login_manager.unauthorized_handler
    # def unauthorized():
    #     app.logger.warning('User unauthorized : URL(%s)' % (request.url))
    #     # do stuff
    #     return redirect(url_for('users.login'))

    # if app.config['BRAINTREE_ENV'] == 'sandbox':
    #     braintree.Configuration.configure(braintree.Environment.Sandbox,
    #                                       merchant_id=app.config[
    #                                           'BRAINTREE_MERCHANT_ID'],
    #                                       public_key=app.config[
    #                                           'BRAINTREE_PUBLIC_KEY'],
    #                                       private_key=app.config['BRAINTREE_PRIVATE_KEY'])
    # elif app.config['BRAINTREE_ENV'] == 'production':
    #     braintree.Configuration.configure(braintree.Environment.Production,
    #                                       merchant_id=app.config[
    #                                           'BRAINTREE_MERCHANT_ID'],
    #                                       public_key=app.config[
    #                                           'BRAINTREE_PUBLIC_KEY'],
    #                                       private_key=app.config['BRAINTREE_PRIVATE_KEY'])
    # else:
    #     app.logger.error('Unknown BRAINTREE_ENV : %s' %
    #                      app.config['BRAINTREE_ENV'])

    # Blueprints
    from app.blueprints.main import main as main_blueprint

    app.register_blueprint(main_blueprint)
  
    # @app.context_processor
    # def insert_login_form():
    #     if current_user.is_authenticated:
    #         passwordChangeForm = PasswordChangeForm()
    #         avatarChangeForm = ProfilePictureForm()
    #         dmForm = DirectMessageForm()
    #         # messages, notifications = current_user.unreadNotifications()
    #         notifications = current_user.getNotifications()
    #         messages = current_user.getMessageNotifications()
    #         houses = current_user.houseList

    #         numUnviewedNotifications = current_user.getUnreadNotificationCount()
    #         numUnviewedMessages = current_user.getUnreadMessageNotificationCount()

    #         return dict(passwordChangeForm=passwordChangeForm,
    #                     avatarChangeForm=avatarChangeForm,
    #                     notifications=notifications,
    #                     numUnviewedNotifications=numUnviewedNotifications,
    #                     numUnviewedMessages=numUnviewedMessages,
    #                     notificationMessages=messages,
    #                     platformReportForm=PlatformReportForm(),
    #                     DirectMessageForm=DirectMessageForm(),
    #                     houses=houses,
    #                     dmForm=dmForm,
    #                     contactForm=ContactForm())
    #     else:
    #         login_form = LoginForm()
    #         dmForm = DirectMessageForm()

    #         return dict(login_form=login_form,
    #                     platformReportForm=PlatformReportForm(),
    #                     dmForm=dmForm,
    #                     contactForm=ContactForm())

    # import nexnest.admin

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

    # @app.context_processor
    # def override_url_for():
    #     return dict(url_for=dated_url_for)

    # def dated_url_for(endpoint, **values):
    #     if endpoint == 'static':
    #         filename = values.get('filename', None)
    #         if filename:
    #             file_path = os.path.join(app.root_path,
    #                                      endpoint, filename)
    #             values['q'] = int(os.stat(file_path).st_mtime)
    #     return url_for(endpoint, **values)

    # CSRF Error Handler
    # from flask_wtf.csrf import CSRFError
    # from flask import abort, flash

    # @app.errorhandler(CSRFError)
    # def handle_csrf_error(e):
    #     app.logger.warning('CSRF error : %r' % e)
    #     flash('CSRF Error. Please go back, refresh the page and try again.', 'warning')
    #     return abort(405)

    return app


# def logEmailDispatch(message, app):
#     app.logger.debug('Email Sent! Subject %s | Text %s' %
#                      (message.subject, message.html))


# email_dispatched.connect(logEmailDispatch)
