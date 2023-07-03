import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_ADMIN_SWATCH = 'cerulean'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')

    @staticmethod
    def init_app(app):
        app.logger.handlers = []
        # log to syslog
        import logging
        import sys
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        app.logger.addHandler(ch)
        pass


class DevelopmentConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

    TESTING = True
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False
    TESTING = False

    # app.logger.handlers = []

    # import logging
    # from logging.handlers import RotatingFileHandler
    # from slack_log_handler import SlackLogHandler

    # # Slack Warning
    # slackWarningHandler = SlackLogHandler(
    #     Config.SLACK_WARNING_URL) or Config.SLACK_LOG_URL
    # slackWarningHandler.setLevel(logging.WARNING)
    # app.logger.addHandler(slackWarningHandler)

    # # Slack Error
    # slackErrHandler = SlackLogHandler(
    #     Config.SLACK_ERROR_URL) or Config.SLACK_LOG_URL
    # slackErrHandler.setLevel(logging.ERROR)
    # app.logger.addHandler(slackErrHandler)

    # # Debug Handler
    # debugHandler = RotatingFileHandler(
    #     '/var/log/nexnest/debug.log', maxBytes=10000, backupCount=5)
    # debugHandler.setLevel(logging.DEBUG)
    # app.logger.addHandler(debugHandler)

    # # Info Handler
    # infoHandler = RotatingFileHandler(
    #     '/var/log/nexnest/info.log', maxBytes=10000, backupCount=5)
    # infoHandler.setLevel(logging.INFO)
    # app.logger.addHandler(infoHandler)

    # MAIL SERVER CONFIG
    # MAIL_SERVER = 'mail.nexnest.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
   
class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler(address='/var/log/app.log')
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'unix': UnixConfig
}
