from flask import Flask
from data.db import db

class CommonApp:
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()


    def home(self):
        return "ok", 200

    def health_check(self):
        return "healthcheck", 200

    def add_routes(self):
        self.app.add_url_rule(
            '/', 'home', self.home, methods=["GET"]
        )
        self.app.add_url_rule(
            '/healthCheck', 'health_check', self.health_check, methods=["GET"]
        )

    def run_server(self):
        self.add_routes()
        self.app.run("0.0.0.0", self.port, debug=True)
