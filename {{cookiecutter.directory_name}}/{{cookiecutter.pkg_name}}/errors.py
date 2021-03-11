__all__ = ['InvalidRequest', 'InputValidation', 'NotFound', 'Accepted',
           'NotAuthorized', 'Forbidden', 'ServiceInternalError', 'Processing']


def http_exception(_status, super_class=Exception):
    class CLABaseHTTPErrorHandler(super_class):

        @property
        def status(self):
            return _status

        @property
        def __dict__(self):
            return {'status': self.status}

    return CLABaseHTTPErrorHandler


InvalidRequest = http_exception(400)
NotFound = http_exception(404, InvalidRequest)
NotAuthorized = http_exception(401, InvalidRequest)
Forbidden = http_exception(403, InvalidRequest)
ServiceInternalError = http_exception(500)
Processing = http_exception(304)
Accepted = http_exception(202)


class InputValidation(InvalidRequest):

    def __init__(self, field, message):
        super(InputValidation, self).__init__('Input validation error')
        self.errors = dict()
        self.errors[field] = message

    @property
    def response(self):
        return dict(errors=self.errors)

    def __add__(self, other):
        self.errors.update(other.errors)

        return self
