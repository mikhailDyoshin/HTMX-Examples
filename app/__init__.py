import os
from typing import Any, Dict
from flask import Flask
from app.bp import navigation


def create_app(test_config: Dict[str, Any] | None = None) -> Flask:
    # create and configure the app
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        instance_relative_config=True,
    )

    app.register_blueprint(navigation.bp)

    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        print(f"Instance folder: {app.instance_path}")
    except OSError:
        print("No instance folder")
        pass

    return app
