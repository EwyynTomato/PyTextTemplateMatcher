from utils.Logger import logging
from flask import Flask, request
from route import ApiRoutes
from utils.AppConfig import config

app = Flask(__name__)
app.register_blueprint(ApiRoutes.apiroutes)
app.logger.addHandler(logging.handlers)
config.setup(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=config.debug, port=config.app_port)