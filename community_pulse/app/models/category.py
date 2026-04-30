from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    questions = relationship('Question', back_populates='category')

    def __repr__(self):
        return f'<Category {self.name}>'
