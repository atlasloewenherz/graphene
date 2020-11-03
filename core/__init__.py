import logging
from logging.config import fileConfig

import yaml
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_graphql_auth import GraphQLAuth
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from healthcheck import EnvironmentDump, HealthCheck
from sqlalchemy import orm

from configs import (Config, DevelopmentConfig, Environments, ProductionConfig,
                     TestingConfig, config_dict)

logger = logging.getLogger(__name__)

''' initialize object references  here'''
blacklist =None
mail = Mail()
db = SQLAlchemy()
flask_bcrypt = Bcrypt()

Session = orm.scoped_session(orm.sessionmaker())

''' FIXME: cors configuration needs to be relative to flask blueprint /uri '''
''' Core configs '''



def create_app(_config):
    
    
    logger.debug("database: {}".format(db))
    app = Flask(__name__)
    if _config is Environments.DEVELOPMENT.value:
        app.config.from_object(DevelopmentConfig())
    elif _config is Environments.TESTING.value:
        app.config.from_object(TestingConfig()) 
    else:
        app.config.from_object(TestingConfig())  
    # TODO: consider more configuration sources
    logging.config.dictConfig(
        yaml.safe_load(app.open_resource(app.config['LOG_CFG_FILE']))
    )
    
    auth = GraphQLAuth(app)
    logger.debug(auth)
    
    # wrap the flask app and give a heathcheck url
    health = HealthCheck(app, "/healthcheck")
    logger.debug(health)
    envdump = EnvironmentDump(app, "/environment")
    logger.debug(envdump)
    if app.config['DEBUG'] is False:
        for key in app.config.keys():
            pass
            logging.debug('KEY \t => \t {} '.format(key) + '\t <=> \t VALUE \t => {} '.format(app.config[key]))
    ''' FIXME: lookup via environ or fall back to default '''
    ''' point to its configuration source '''
    cors = CORS(app, resources={r"/graphql/*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    ''' enable encryption via '''
    flask_bcrypt.init_app(app)
    blacklist = set()
    
    #configs.init_app(app)
    ''' Set up extensions '''
    mail.init_app(app)

    #logging.debug(logging)
    db.init_app(app)
    # app.config_dict['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' see configuration
    migrate = Migrate(app, db)
    with app.app_context():
        from help.graphql.user.models import User
        Session.configure(bind=db)
        db.create_all()
        from help.graphql import SchemaBuilder
        sb = SchemaBuilder()
        schema = sb.build()
        if schema:
            #ogger.debug(schema)
            app.add_url_rule(
             '/graphql',
             view_func=GraphQLView.as_view(
             'graphql',
             schema=schema,
             graphiql=True, # for having the GraphiQL interface
             get_context=lambda: {'session':Session}
            )
            )
        #logger.info(schema)
       
    return app

