import click
from app import create_app
from app.models import db, Category, Question

app = create_app()

@app.cli.command("seed-db")
def seed_db_command():
    """Заполняет базу данных начальными данными."""
    # Удаляем все существующие данные, чтобы избежать дубликатов
    db.drop_all()
    db.create_all()

    # --- Создание категорий ---
    print("Создание категорий...")
    cat1 = Category(name="Общие вопросы")
    cat2 = Category(name="Технические вопросы")
    cat3 = Category(name="Предложения")
    db.session.add_all([cat1, cat2, cat3])
    db.session.commit()
    print("Категории созданы.")

    # --- Создание вопросов ---
    print("Создание вопросов...")
    q1 = Question(text="Какой сегодня день?", category_id=cat1.id)
    q2 = Question(text="Как настроить Flask-Migrate?", category_id=cat2.id)
    q3 = Question(text="Почему небо голубое?", category_id=cat1.id)
    q4 = Question(text="Предлагаю добавить новую фичу.", category_id=cat3.id)
    q5 = Question(text="Что такое REST API?", category_id=cat2.id)
    db.session.add_all([q1, q2, q3, q4, q5])
    db.session.commit()
    print("Вопросы созданы.")

    print("\nБаза данных успешно заполнена!")


if __name__ == '__main__':
    app.run(debug=True)
