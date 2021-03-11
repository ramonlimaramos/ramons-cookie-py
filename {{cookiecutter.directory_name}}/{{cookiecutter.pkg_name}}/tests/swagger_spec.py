

class SwaggerSpec:

    def when_download_swagger_json(self):
        raise NotImplementedError()

    def assert_ok(self):
        raise NotImplementedError()

    def test_download_of_swagger_file(self):
        self.when_download_swagger_json()
        self.assert_ok()