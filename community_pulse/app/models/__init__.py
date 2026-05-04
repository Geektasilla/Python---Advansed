# Импортируем db из центрального файла extensions
from ..extensions import db

# Теперь импортируем модели, чтобы SQLAlchemy мог их обнаружить
from .response import Response
from .questions import Question, Statistic
from .category import Category
