import os

# Определяем базовую директорию проекта
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    # Указываем полный путь к файлу базы данных
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'community_pulse.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Рекомендуется для отключения лишних уведомлений

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
