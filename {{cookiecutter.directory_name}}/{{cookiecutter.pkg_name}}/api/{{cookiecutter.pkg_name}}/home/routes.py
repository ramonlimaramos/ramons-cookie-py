from flask_restx import Resource
from {{cookiecutter.pkg_name}}.api.{{cookiecutter.pkg_name}}.home.definition import ns
from {{cookiecutter.pkg_name}}.api.{{cookiecutter.pkg_name}}.home.marshalling import success_result


@ns.doc('Home resource swagger doc')
@ns.route('/')
class HomeController(Resource):

    @ns.doc('get home')
    @ns.response(200, 'Successful executed the method get', model=success_result)
    def get(self):
        return {'status': 'OK', 'message': 'Hello ramons-cookie-py'}, 200