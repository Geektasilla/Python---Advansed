# Python Advanced: Домашнее задание 4
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base
# Задача 1: Наполнение данными
# Добавьте в базу данных следующие категории и продукты
# Добавление категорий: Добавьте в таблицу categories следующие категории:
# Название: "Электроника", Описание: "Гаджеты и устройства."
# Название: "Книги", Описание: "Печатные книги и электронные книги."
# Название: "Одежда", Описание: "Одежда для мужчин и женщин."
# Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан с соответствующей категорией:
# Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
# Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
# Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
# Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
# Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Numeric(10, 2))
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="products")

engine = create_engine('sqlite:///database.db')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


if not session.query(Category).first():
    session.add_all([
        Category(name='Электроника', description='Гаджеты и устройства'),
        Category(name='Книги', description='Печатные книги и электронные книги'),
        Category(name='Одежда', description='Одежда для мужчин и женщин.')
    ])
    session.commit()

if not session.query(Product).first():
    electronics_cat = session.query(Category).filter_by(name='Электроника').first()
    books_cat = session.query(Category).filter_by(name='Книги').first()
    clothes_cat = session.query(Category).filter_by(name='Одежда').first()

    session.add_all([
        Product(name='Смартфон', price=299.99, in_stock=True, category=electronics_cat),
        Product(name='Ноутбук', price=499.99, in_stock=True, category=electronics_cat),
        Product(name='Научно-фантастический роман', price=15.99, in_stock=True, category=books_cat),
        Product(name='Джинсы', price=40.50, in_stock=True, category=clothes_cat),
        Product(name='Футболка', price=20.00, in_stock=True, category=clothes_cat)
    ])
    session.commit()

# Задача 2: Чтение данных
# Извлеките все записи из таблицы categories.
# Для каждой категории извлеките и выведите все связанные с ней продукты,
# включая их названия и цены.

all_categories = session.query(Category).all()
for category in all_categories:
    print(f"Категория: {category.name}")
    products_in_category = session.query(Product).filter(Product.category_id == category.id).all()
    if category.products:
        for product in category.products:
            print(f"Название: {product.name}, Цена: {product.price}")
    else:
        print("Продуктов нет")

# Задача 3: Обновление данных
# Найдите в таблице products первый продукт с названием "Смартфон".
# Замените цену этого продукта на 349.99.

product_to_update = session.query(Product).filter_by(name='Смартфон').first()
if product_to_update:
    print(f"Старая цена смартфона: {product_to_update.price}")
    product_to_update.price = 349.99
    session.commit()
    # Можно даже так, через relationship, проверить категорию
    print(f"Новая цена смартфона: {product_to_update.price} (Категория: {product_to_update.category.name})")

# Задача 4: Агрегация и группировка
# Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.

product_counts = session.query(
    Category.name,
    func.count(Product.id)
).join(Product).group_by(Category.name).all()
print(product_counts)


# Задача 5: Группировка с фильтрацией
# Отфильтруйте и выведите только те категории, в которых более одного продукта.
categories_with_more_than_one_product = session.query(
    Category.name,
    func.count(Product.id)
).join(Product).group_by(Category.name).having(func.count(Product.id) > 1).all()
print(categories_with_more_than_one_product)

session.close()
