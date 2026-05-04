from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from ..extensions import db  # Изменено
from ..models import Question, Category
from ..schemas.question import QuestionCreate, QuestionResponse, QuestionOut
from sqlalchemy.orm import joinedload

# Создаем Blueprint для вопросов
questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов."""
    questions = db.session.query(Question).options(joinedload(Question.category)).all()

    # questions = [QuestionResponse.model_validate(q).model_dump() for q in questions]
    return jsonify([QuestionOut.model_validate(q).model_dump() for q in questions]), 200


@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json()
    try:
        question_data = QuestionCreate(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    new_question = Question(text=question_data.text)

    if question_data.category_id:
        category = db.session.get(Category, question_data.category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        new_question.category = category  # Связываем вопрос с категорией

    db.session.add(new_question)
    db.session.commit()

    db.session.refresh(new_question)
    return jsonify(QuestionOut.model_validate(new_question).model_dump()), 201


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
        if 'category_id' in data:
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
