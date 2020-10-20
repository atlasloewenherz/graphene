import os
import tempfile

import pytest

from core import create_app
from configs import Environments

devconfig = Environments.TESTING

testing_config = devconfig.value


@pytest.fixture
def app():
    app = create_app(os.getenv('FLASK_CONFIG') or testing_config)
    return app

