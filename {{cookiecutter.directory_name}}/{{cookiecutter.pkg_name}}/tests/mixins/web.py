from flask import Flask

__all__ = ['HttpMixin', 'JsonMixin', 'FlaskMixin']


def have_response(func):

    def wrapper(self, *args, **kwargs):
        self.assertTrue(hasattr(self, 'response'), 'must have a response')
        return func(self, *args, **kwargs)

    return wrapper


class HttpMixin:

    def _print_error_message(self):
        if self.response.status_code >= 400 and self.response.is_json:
            return self.response.json

    @have_response
    def assert_status_code(self, *status_code):
        self.assertIn(self.response.status_code, status_code,
                      self._print_error_message())

    def assert_ok(self):
        self.assert_status_code(200)

    def assert_created(self):
        self.assert_status_code(201)

    def assert_accecpted(self):
        self.assert_status_code(202)

    def assert_not_modified(self):
        self.assert_status_code(304)

    def assert_bad_request(self):
        self.assert_status_code(400)

    def assert_unauthorized(self):
        self.assert_status_code(401)

    def assert_forbidden(self):
        self.assert_status_code(403)

    def assert_not_found(self):
        self.assert_status_code(404)


class JsonMixin(HttpMixin):

    @have_response
    def assert_response_count(self, count, status_code=200):
        self.assert_status_code(status_code)
        self.assertEqual(len(self.response.json), count)

    @have_response
    def assert_response_has(self, index=None, status_code=[200, 201], **kwargs):
        self.assert_status_code(*status_code)
        data = self.response.json
        if index is not None:
            data = data[index]
        for k, v in kwargs.items():
            breadcrumb = k.split('__')
            if len(breadcrumb) == 1:
                self.assertIn(k, data)
                self.assertEqual(data[k], v)
            else:
                self.assertIn(breadcrumb[0], data)
                actual = data[breadcrumb[0]]
                for move in breadcrumb[1:]:
                    if type(actual) == list:
                        actual = actual[int(move)]
                    else:
                        self.assertIn(move, actual)
                        actual = actual[move]
                self.assertEqual(actual, v)

    @have_response
    def assert_response_has_not(self, field, index=None, status_code=[200, 201]):
        self.assert_status_code(*status_code)
        data = self.response.json
        if index is not None:
            data = data[index]

        breadcrumb = field.split('__')
        if len(breadcrumb) == 1:
            self.assertNotIn(field, data)
        else:
            has_field = False
            if breadcrumb[0] in data:
                has_field = True
            actual = data[breadcrumb[0]]
            for move in breadcrumb[1:]:
                if type(actual) == list:
                    actual = actual[int(move)]
                else:
                    if move in actual:
                        actual = actual[move]
                        has_field = True
                    else:
                        has_field = False

            self.assertFalse(has_field)

    def assert_response_not_none(self, field, index=0):
        data = self.response.json
        if index is not None:
            data = data[index]
        breadcrumb = field.split('__')
        if len(breadcrumb) == 1:
            self.assertIn(field, data)
            self.assertIsNotNone(data[field])
        else:
            raise NotImplementedError()

    def assert_bad_request(self, **kwargs):
        self.assert_response_has(status_code=[400], **kwargs)


class WebClientMixin(JsonMixin):

    @property
    def headers(self):
        headers = {} if not hasattr(self, 'http_headers') else self.http_headers

        if hasattr(self, 'access_token') and self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers


class FlaskMixin(object):
    _client = None

    def flask_set_up(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self._client = self.app.test_client()
        self.app.config['SECRET_KEY'] = 'secret'

    @property
    def client(self):
        if not self._client:
            raise NotImplementedError()
        return self._client