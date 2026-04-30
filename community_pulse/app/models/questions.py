from . import db

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    # Добавляем внешний ключ для связи с категорией
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    responses = db.relationship('Response', backref='question', lazy=True)
    # Добавляем связь с моделью Category, используя строковое имя
    category = db.relationship('Category', back_populates='questions')

    def __repr__(self):
        return f'Question: {self.text}'

class Statistic(db.Model):
    __tablename__ = 'statistics'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Statistic for Question %r: %r agree, %r disagree>' % (self.question_id, self.agree_count, self.disagree_count)