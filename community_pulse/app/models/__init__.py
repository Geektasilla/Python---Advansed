from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .response import Response
from .questions import Question, Statistic
from .category import Category # Добавляем импорт для новой модели Category
