from flask_restx import Namespace

__all__ = ['ns']

ns = Namespace(
    'home', description='This is your home api endpoint', 
    # authorization config
    # authorizations={
    #     'apikey': {
    #         'type': 'apiKey',
    #         'in': 'header',
    #         'name': 'Authorization',
    #         'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    #     },
    # }
    )