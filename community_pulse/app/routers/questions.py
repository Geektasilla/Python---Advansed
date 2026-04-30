from flask import Blueprint, request, jsonify
# from pydantic import ValidationError # Больше не используется в этом файле
from app.models import db, Question, Category
# from app.schemas.question import QuestionUpdate, QuestionOut # QuestionUpdate больше не используется
from app.schemas.question import QuestionOut # Оставляем QuestionOut для других эндпоинтов
from typing import List

# Создаем Blueprint для вопросов
questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов с их категориями."""
    questions = db.session.query(Question).all()
    questions_out = [QuestionOut.from_orm(q).dict() for q in questions]
    return jsonify(questions_out)

@questions_bp.route('/', methods=['POST'])
def create_question():
    """Создание нового вопроса."""
    data = request.get_json()

    if not data or not data.get('text'):
        return jsonify({'error': 'No question text provided'}), 400

    text = data['text']
    category_id = data.get('category_id') # Получаем category_id, если он есть

    # Опционально: можно добавить проверку существования категории
    if category_id is not None:
        category = db.session.query(Category).get(category_id)
        if category is None:
            return jsonify({'error': f'Category with id {category_id} not found'}), 400

    question = Question(text=text, category_id=category_id)
    db.session.add(question)
    db.session.commit()
    db.session.refresh(question) # Обновляем объект, чтобы получить id и связанные данные

    # Возвращаем созданный вопрос, используя QuestionOut для форматирования
    return jsonify(QuestionOut.from_orm(question).dict()), 201

@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """Получение деталей конкретного вопроса по его ID."""
    question = db.session.query(Question).filter(Question.id == id).one_or_none()
    if question is None:
        return jsonify({"message": "Вопрос не найден"}), 404

    return jsonify({'message': f"Вопрос: {question.text}"}), 200

@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """Обновление конкретного вопроса по его ID."""

    question = db.session.query(Question).filter(Question.id == id).one_or_none()
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    data = request.get_json()

    if data and data.get('text'):
        question.text = data['text']
        # Добавим обновление категории, если оно есть в запросе
        if 'category_id' in data:
            # Можно добавить проверку существования категории, как в create_question
            category_id = data['category_id']
            if category_id is not None:
                category = db.session.query(Category).get(category_id)
                if category is None:
                    return jsonify({'error': f'Category with id {category_id} not found'}), 400
            question.category_id = category_id
        db.session.commit()
        return jsonify({'message': f"Вопрос обновлен: {question.text}"}), 200

    return jsonify({'message': "Текст вопроса не предоставлен"}), 400

@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Удаление конкретного вопроса по его ID."""

    question = db.session.query(Question).filter(Question.id == id).one_or_none()
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f"Вопрос с ID {id} удален"}), 200
