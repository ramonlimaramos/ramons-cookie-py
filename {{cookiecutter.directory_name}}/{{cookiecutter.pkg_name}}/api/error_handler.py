from sqlalchemy.orm.exc import NoResultFound
from {{cookiecutter.pkg_name}}.errors import InvalidRequest, InputValidation, NotAuthorized, NotFound, Forbidden
from .api_definition import api_def


@api_def.errorhandler(InvalidRequest)
def handle_bad_request(e):
    if isinstance(e, InputValidation):
        return e.response, e.status
    return {}, e.status


@api_def.errorhandler(NoResultFound)
def handle_no_result_found(e):
    return {}, 404


@api_def.errorhandler(NotFound)
def handle_no_result_found(e):
    return {}, e.status


@api_def.errorhandler(NotAuthorized)
def handle_not_authorized(e):
    return {}, e.status

@api_def.errorhandler(Forbidden)
def handle_forbidden(e):
    return {}, e.status