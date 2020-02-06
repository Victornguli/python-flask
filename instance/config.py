import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
	"""Parent configuration class"""
	DEBUG = False
	CSRF_ENABLED = True
	SECRET = os.getenv('SECRET')
	SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(BaseConfig):
	"""Configuration for development"""
	DEBUG = True


class TestingConfig(BaseConfig):
	"""Configurations for testing, with a separate database"""
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_TEST_DATABASE_URI')
	DEBUG = True


class StagingConfig(BaseConfig):
	"""Configuration for staging environment"""
	DEBUG = True


class ProductionConfig(BaseConfig):
	"""Configurations for Production environment"""
	DEBUG = False
	TESTING = False


app_config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'staging': StagingConfig,
	'production': ProductionConfig,
}
