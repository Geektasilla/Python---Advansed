from flask import Flask

# Создаем экземпляр приложения
app = Flask(__name__)

# Маршрут для корневого URL (/)
@app.route('/')
def home():
    return 'Hello, Flask!'

# Маршрут для /user/<name>
@app.route('/user/<name>')
def hello_user(name):
    # Мы используем f-строку для подстановки имени
    return f'Hello, {name}!'

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)