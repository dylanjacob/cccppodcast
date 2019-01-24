
from flask_testing import TestCase

from lib import create_app

app = create_app()

class BaseTestCase(TestCase):


    def create_app(self):
        return app
