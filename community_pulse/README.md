# Community Pulse API

Это API для проекта "Community Pulse", созданное с использованием Flask.

## Структура проекта

```
/community_pulse/
|-- app/
|   |-- __init__.py
|   |-- migrations/
|   |-- models/
|   |   |-- __init__.py
|   |   |-- category.py
|   |   |-- questions.py
|   |   `-- response.py
|   |-- routers/
|   |-- schemas/
|-- config.py
|-- run.py
|-- community_pulse.db
`-- README.md
```

## Как запустить приложение

### 1. Установка зависимостей

Убедитесь, что у вас активирована виртуальная среда и установлены все необходимые пакеты.

```bash
pip install -r requirements.txt
```
*(Примечание: если у вас нет файла `requirements.txt`, вы можете создать его командой `pip freeze > requirements.txt`)*

### 2. Настройка переменных окружения

Для корректной работы Flask необходимо указать главный файл приложения.

**В Windows (Command Prompt):**
```bash
set FLASK_APP=run.py
```

**В Windows (PowerShell):**
```bash
$env:FLASK_APP="run.py"
```

**В macOS/Linux:**
```bash
export FLASK_APP=run.py
```

### 3. Работа с базой данных (миграции)

Перед первым запуском или после изменения моделей необходимо создать и применить миграции.

**Если вы начинаете с нуля:**
```bash
# 1. Инициализация (только один раз для нового проекта)
python -m flask db init

# 2. Создание первой миграции
python -m flask db migrate -m "Initial migration"

# 3. Применение миграции к базе данных
python -m flask db upgrade
```

**Если вы изменили модели в существующем проекте:**
```bash
# 1. Создание новой миграции
python -m flask db migrate -m "Краткое описание изменений"

# 2. Применение миграции
python -m flask db upgrade
```

### 4. Запуск приложения

Теперь можно запустить сервер для разработки.

```bash
python -m flask run
```

Приложение будет доступно по адресу `http://127.0.0.1:5000`.

### Доступные эндпоинты:
- **`http://127.0.0.1:5000/questions/`** - для работы с вопросами.
- **`http://127.0.0.1:5000/responses/`** - для работы с ответами.
```