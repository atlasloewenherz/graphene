#!/usr/bin/env python
import logging
import os
import subprocess

from flask_script import Manager, Shell  

from configs import Environments
from core import create_app, db
# TODO: only in Testing/Dev environment

from flask_migrate import Migrate, MigrateCommand
#from modules.user.models import User

devconfig = Environments.DEVELOPMENT

default_config = devconfig.value

logger = logging.getLogger(__name__)

# app = create_app(Environments.DEVELOPMENT.value)
logging.info("FASK_CONFIG from The Environment: {} ".format(os.getenv('FLASK_CONFIG')))
app = create_app(os.getenv('FLASK_CONFIG') or default_config)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app)


manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.option('-n',
                '--number-users',
                default=10,
                type=int,
                help='Number of each model type to create',
                dest='number_users')
@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


@manager.command
def server():
    #db.create_all()
    app.run(port=8888)


@manager.command
def populate():
    logging.info('ping')
    for i in range(5, 200):
        try:
            u = UserFactory.create()
            ua = AddressFactory.create()
            u.addresses.append(ua)
            logging.info(u)

            p = PartyFactory.create()
            pa = AddressFactory.create()
            p.addresses.append(pa)
            logging.info(p)
            db.session.commit()
        except Exception as e:
            logging.error(e)
            exit()
    db.session.flush()



@manager.command
def createdb():
    ''' Create the database '''
    create_app(devconfig.value)

if __name__ == '__main__':
    manager.run()

