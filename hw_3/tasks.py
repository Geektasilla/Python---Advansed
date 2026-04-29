# Python Advanced: Домашнее задание 3.
# Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
# Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.
# Задача 3: Определите модель продукта Product со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# price: числовое значение с фиксированной точностью
# in_stock: логическое значение
# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# description: строка (макс. 255 символов)
# Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.

import sqlalchemy
from sqlalchemy import create_engine, Column, Numeric, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(10,2))
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='products')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))

    products = relationship('Product', back_populates='category')


engine = sqlalchemy.create_engine('sqlite:///my_database.db')
# engine = create_engine('sqlite:///:memory:')

# Создаем класс Session, который будет использоваться для взаимодействия с БД
Session = sessionmaker(bind=engine)
# Создаем экземпляр сессии
session = Session()

# для проверки

# 1. Создаем таблицы в базе данных
# Эта команда смотрит на все классы, унаследованные от Base, и создает для них таблицы.
Base.metadata.create_all(engine)
# 2. Создаем экземпляры (объекты)
# Создаем категорию
category1 = Category(name='Электроника', description='Гаджеты и устройства')
# Создаем продукт и сразу связываем его с категорией
product1 = Product(name='Смартфон', price=599.99, in_stock=True, category=category1)
product2 = Product(name='Ноутбук', price=5999.99, in_stock=True, category=category1)
# 3. Добавляем объекты в сессию
session.add(category1)
session.add(product1)
session.add(product2)
# 4. Сохраняем изменения в базе данных
session.commit()

print(*[p.name for p in category1.products], sep='\n')
print(product1.category.name)

session.close()

