import os

from flask import Flask


def create_app(test_config=None):
    # cria e configura o aplicativo
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None:
        # carrega a instancia de config, se ela existir, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # carrega a test config se for passada
        app.config.from_mapping(test_config)

    # assegura que o diretorio de instancia existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # pagina simples que diz Olá
    @app.route('/hello')
    def hello():
        return 'Olá, mundo!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
