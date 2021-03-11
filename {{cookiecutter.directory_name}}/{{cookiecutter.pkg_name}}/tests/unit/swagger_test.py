from unittest import TestCase
from flask import Flask
from {{cookiecutter.pkg_name}}.api import api
from {{cookiecutter.pkg_name}}.tests.swagger_spec import SwaggerSpec
from {{cookiecutter.pkg_name}}.tests.mixins import JsonMixin

class SwaggerTest(JsonMixin, SwaggerSpec, TestCase):

    def setUp(self):
        super(SwaggerTest, self).setUp()
        self.app = Flask(__name__)
        self.app.register_blueprint(api, url_prefix='/')
        self.client = self.app.test_client()

    def tearDown(self):
        super(SwaggerTest, self).tearDown()

    def when_download_swagger_json(self):
        self.response = self.client.get('/swagger.json')
