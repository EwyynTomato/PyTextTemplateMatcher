from utils.Logger import logging
from flask import Flask
from route import ApiRoutes
from utils.AppConfig import config

app = Flask(__name__)
app.register_blueprint(ApiRoutes.apiroutes)
app.logger.addHandler(logging.handlers)
config.setup(app)

if __name__ == '__main__':
    import threading, webbrowser
    threading.Timer(2, lambda: webbrowser.open("http://{:}:{:}/".format(config.app_host, config.app_port)))\
        .start() #Delayed open the website in default browser
    app.run(host=config.app_host, debug=config.debug, port=config.app_port)
