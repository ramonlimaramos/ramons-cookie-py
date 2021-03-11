from .base import api, CustomAPI
from .{{cookiecutter.pkg_name}}.home import ns as home_ns

api_def = CustomAPI(api,
            title='{{cookiecutter.project_name}} API',
            version='0.1.0',
            description='{{cookiecutter.description}}',
          )

api_def.add_namespace(home_ns)
