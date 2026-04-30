from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .category import CategoryOut # Импортируем схему для категории

class QuestionBase(BaseModel):
    text: str = Field(..., min_length=3, description="Текст вопроса")
    category_id: Optional[int] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(BaseModel):
    id: int
    text: str
    
    model_config = ConfigDict(
        from_attributes=True
    )

class QuestionOut(QuestionBase):
    id: int
    category: Optional[CategoryOut] = None # Включаем вложенную схему категории

    model_config = ConfigDict(
        from_attributes=True
    )
