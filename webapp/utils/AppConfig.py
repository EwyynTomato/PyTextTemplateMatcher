class AppConfig(object):
    def __init__(self):
        self.config = None

    def setup(self, app, config_file_path='config/application.cfg'):
        app.config.from_pyfile(config_file_path)
        self.config = app.config

    @property
    def debug(self):
        return self.config["IS_DEBUG"]

    @property
    def app_host(self):
        return self.config["APP_HOST"]

    @property
    def app_port(self):
        return self.config["APP_PORT"]

config = AppConfig()
