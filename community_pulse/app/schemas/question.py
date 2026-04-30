from pydantic import BaseModel
from typing import Optional
from .category import CategoryOut # Импортируем схему для категории

class QuestionBase(BaseModel):
    text: str
    category_id: Optional[int] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(QuestionBase):
    id: int
    category: Optional[CategoryOut] = None # Включаем вложенную схему категории

    class Config:
        from_attributes = True
