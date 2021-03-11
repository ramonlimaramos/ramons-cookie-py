from {{cookiecutter.pkg_name}}.web import create_app


app = create_app()


if __name__ == "__main__":
    app.run()