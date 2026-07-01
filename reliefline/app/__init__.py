from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    mysql.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.prediction import prediction_bp
    from app.routes.allocation import allocation_bp
    from app.routes.warehouse import warehouse_bp
    from app.routes.preposition import preposition_bp
    from app.routes.distribution import distribution_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(allocation_bp)
    app.register_blueprint(warehouse_bp)
    app.register_blueprint(preposition_bp)
    app.register_blueprint(distribution_bp)

    return app