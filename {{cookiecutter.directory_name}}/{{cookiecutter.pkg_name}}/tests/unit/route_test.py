from unittest import TestCase
from flask import Flask
from {{cookiecutter.pkg_name}}.tests.mixins import JsonMixin
from {{cookiecutter.pkg_name}}.api import api


class RouteTest(JsonMixin, TestCase):

    def setUp(self):
        super(RouteTest, self).setUp()
        self.app = Flask(__name__)
        self.app.register_blueprint(api, url_prefix='/')
        self.client = self.app.test_client()

    def tearDown(self):
        super(RouteTest, self).tearDown()

    def when_acess_home(self):
        self.response = self.client.get('/home/')
    
    def test_api_home_route_is_up(self):
        self.when_acess_home()
        self.assert_ok()
        self.assert_response_has(message='Hello ramons-cookie-py')
