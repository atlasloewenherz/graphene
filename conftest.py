import os

import pytest

from configs import Environments

from core import create_app

devconfig = Environments.TESTING

testing_config = devconfig.value


@pytest.fixture()
def app():
    app = create_app(os.getenv('FLASK_CONFIG') or testing_config)
    return app

