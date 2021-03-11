from flask import Flask, url_for
from {{cookiecutter.pkg_name}}.api import api
from flask_restx import apidoc
from os.path import dirname, join
from urllib.parse import urlparse, parse_qs
from sqlalchemy import create_engine


custom_apidoc = apidoc.Apidoc(
    'custom_restx_doc',
    __name__,
    template_folder='templates',
    static_folder=join(dirname(apidoc.__file__), 'static'),
    static_url_path='/api/swaggerui',
)


DATABASE_URL = 'sqlite:///db.sqlite'


@custom_apidoc.add_app_template_global
def swagger_static(filename):
    return url_for("custom_restx_doc.static", filename=filename)


def create_database(config=None):
    engine = create_engine(DATABASE_URL, convert_unicode=True)
    Base.metadata.create_all(engine)


def bind_database():
    parsed = urlparse(DATABASE_URL)
    kwargs = {}
    if parsed.scheme in ['postgres', 'postgresql']:
        kwargs['pool_size'] = 10
        kwargs['max_overflow'] = 10
        kwargs['pool_recycle'] = 3600
        query = parse_qs(parsed.query)
        if 'sslmode' in query:
            kwargs['connect_args'] = {'sslmode': query['sslmode'][0]}

    engine = create_engine(DATABASE_URL, convert_unicode=True, **kwargs)
    db_session.configure(bind=engine)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api/v1')
    app.register_blueprint(custom_apidoc)

    return app
