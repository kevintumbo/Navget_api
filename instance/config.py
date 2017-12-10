import os


class Config(object):
    """ Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET') or 'this-is-a-secret-key'
    MONGODB_DB = 'navyget_api'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    MONGODB_DB = 'test_navy_api'
    MONGODB_PORT = 'localhost'
    MONGODB_PORT = 27017
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
