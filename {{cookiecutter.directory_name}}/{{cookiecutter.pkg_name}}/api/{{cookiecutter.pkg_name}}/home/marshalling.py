from flask_restx import fields
from {{cookiecutter.pkg_name}}.api.{{cookiecutter.pkg_name}}.home.definition import ns

success_result = ns.model('success_result', {
    'status': fields.String,
    'message': fields.String,
})