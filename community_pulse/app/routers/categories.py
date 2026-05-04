from flask import Blueprint, request, jsonify
from ..models.category import Category
from ..schemas.question import CategoryBase
from ..schemas.category import CategoryOut
from ..extensions import db

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

# эндпоинты для категорий

@categories_bp.route('/', methods=['POST'])
def create_category():
    """Создание новой категории."""
    data = request.get_json()
    try:
        category_data = CategoryBase(**data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    new_category = Category(name=category_data.name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify(CategoryOut.model_validate(new_category).model_dump()), 201

@categories_bp.route('/', methods=['GET'])
def get_category():
    """Получение списка всех категорий."""
    categories = Category.query.all()
    return  jsonify([CategoryOut.model_validate(cat).model_dump() for cat in categories]), 200

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_single_category(category_id):
    """Получение одной категории по ID."""
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(CategoryOut.model_validate(category).model_dump()), 200


@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Обновление категории по ID."""
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    data = request.get_json()
    try:
        category_data = CategoryBase(**data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    category.name = category_data.name
    db.session.commit()
    return jsonify(CategoryOut.model_validate(category).model_dump()), 200


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Удаление категории по ID."""
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': 'Category deleted'}), 200
