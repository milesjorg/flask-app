import os, datetime

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=60)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Flask-Login settings
    LOGIN_DISABLED = False
    LOGIN_USER_TEMPLATE = "auth/login.html"
    LOGIN_MANAGER = "login_manager"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def get_config(app_name):
    return config_by_name.get(app_name, DevelopmentConfig)

