import os

folder_path = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mailgun.org')
    MAIL_PORT = os.getenv('MAIL_SERVER_PORT', 2525)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    SENTRY_DSN = os.getenv('SENTRY_DSN')

    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_k1')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'sk_test_k1')
    STRIPE_WEBHOOK_KEY = os.getenv('STRIPE_WEBHOOK_KEY', 'sk_test_k1')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RQ_REDIS_URL = REDIS_URL
    RQ_DASHBOARD_REDIS_URL =  RQ_REDIS_URL


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(folder_path, 'dev.db'))
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY', '00000abcdef')
    SQLALCHEMY_ECHO = True
    # Don't do anything fancy with the assets pipeline (faster + easier to debug)
    ASSETS_DEBUG = True
    RQ_REDIS_URL = REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE = 'simple'
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(folder_path, 'test.db'))
    SECRET_KEY = os.getenv('YUMROAD_SECRET_KEY', '12345abcdef')
    WTF_CSRF_ENABLED = False
    STRIPE_WEBHOOK_KEY = 'whsec_test_secret'
    ASSETS_DEBUG = True
    # Run jobs instantly, without needing to spin up a worker
    RQ_ASYNC = False
    RQ_CONNECTION_CLASS = 'fakeredis.FakeStrictRedis'
    DEBUG_TB_ENABLED = False
    CACHE_TYPE = 'null'
    CACHE_NO_NULL_WARNING = True

class ProdConfig(BaseConfig):
    DEBUG = False
    SESSION_PROTECTION = "strong"
    # You should be using HTTPS in production anyway, but if you are not, turn
    # these two off
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    ASSETS_DEBUG = False
    RQ_REDIS_URL = REDIS_URL = os.getenv('REDIS_URL')
    RQ_ASYNC = (REDIS_URL is not None)
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'yumroad-'

configurations = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
