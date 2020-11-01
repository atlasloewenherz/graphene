import os
import sys
import tempfile
from enum import Enum
import logging

logger = logging.getLogger(__name__)

PYTHON_VERSION = sys.version_info[0]

if PYTHON_VERSION == 3:
    import urllib.parse
else:
    import urlparse

if os.path.exists('config_dict.env'):
    print('Importing environment from .env file')
    for line in open('config_dict.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Environments(Enum):
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PROD = 'production'
    DEFAULT = 'default'
    HEROKU = 'heroku'
    UNIX = 'unix'


class Config:
    ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = False
    # TODO: create default logging configurations here
    LOG_CFG_FILE = '../configs/logging.yaml'
    LOG_TYPE = os.environ.get("LOG_TYPE", "watched")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
    APP_NAME = os.environ.get('APP_NAME', 'MEMORIS')
    REFRESH_EXP_LENGTH = 30
    ACCESS_EXP_LENGTH = 10
    JWT_SECRET_KEY = 'this_is_not_set_yet'
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
        JWT_SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        JWT_SECRET_KEY = 'this_is_the_default'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')

    DB_NAME = 'default_database.db'

    @property
    def DB_URI(self):
        DB_TEMP = tempfile.gettempdir()
        DB_PATH = os.path.join(os.path.dirname(DB_TEMP), self.DB_NAME)
        logger.info("sqlite:///{}".format(DB_PATH))
        return "sqlite:///{}".format(DB_PATH)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin account
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'elassad@users.sourceforge.net')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = False
    DEBUG = True
    DB_NAME = 'dev_database.db'
    DB_TEMP = tempfile.gettempdir()
    SECRET_KEY = "longswayhomeoverthebridgethatcanwingyouoverall"
    SECURITY_PASSWORD_SALT = "asasa23232asasas1212asasas928iusdc"

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    SQLALCHEMY_ECHO = False
    DEBUG = True
    DB_NAME = 'test_database.db'
    DB_TEMP = tempfile.gettempdir()
    SECRET_KEY = "longswayhomeoverthebridgethatcanwingyouoverall"
    SECURITY_PASSWORD_SALT = "asasa23232asasas1212asasas928iusdc"
    TESTING = True
    ENV = Environments.TESTING.value

    #    logfile = logging.getLogger('file')
    #    logconsole = logging.getLogger('console')
    #    logfile.debug("Debug FILE")
    #    logconsole.debug("Debug CONSOLE")

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    USE_RELOADER = False

    SSL_DISABLE = (os.environ.get('SSL_DISABLE', 'True') == 'True')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'
        ##flask_raygun.Provider(app, app.config_dict['RAYGUN_APIKEY']).attach()


class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig
}
