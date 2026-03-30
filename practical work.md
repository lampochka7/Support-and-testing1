Я помогу вам выполнить эту практическую работу по написанию интеграционных тестов в pytest. Давайте создадим все необходимые файлы и тесты.

## Структура проекта

Сначала создадим все директории и файлы:

```
project/
├── app/
│   ├── __init__.py
│   ├── repository.py
│   ├── api.py
│   └── files.py
├── tests/
│   ├── __init__.py
│   └── integration/
│       ├── __init__.py
│       ├── test_repository.py
│       ├── test_api.py
│       └── test_files.py
├── conftest.py
└── pytest.ini
```

## Часть 2. Код приложения

### app/repository.py
```python
import sqlite3

def init_db(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    connection.commit()

def add_user(connection, name):
    connection.execute("INSERT INTO users (name) VALUES (?)", (name,))
    connection.commit()

def get_user_by_name(connection, name):
    cursor = connection.execute("SELECT id, name FROM users WHERE name = ?", (name,))
    return cursor.fetchone()

def get_all_users(connection):
    cursor = connection.execute("SELECT id, name FROM users")
    return cursor.fetchall()
```

### app/api.py
```python
from flask import Flask, request, jsonify

users = []

def create_app():
    app = Flask(__name__)
    
    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.get_json()
        users.append(data)
        return jsonify(data), 201
    
    @app.route("/users", methods=["GET"])
    def list_users():
        return jsonify(users), 200
    
    return app
```

### app/files.py
```python
def save_report(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def read_report(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
```

### app/__init__.py
```python
# Пустой файл для обозначения пакета
```

## Часть 3. Настройка pytest

### pytest.ini
```ini
[pytest]
markers =
    integration: integration tests
    db: database integration tests
    api: api integration tests
    files: filesystem integration tests

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### conftest.py
```python
import sqlite3
import pytest
import tempfile
import os
from app.repository import init_db
from app.api import create_app, users

@pytest.fixture
def db_connection():
    """Фикстура для создания временной базы данных в памяти"""
    connection = sqlite3.connect(":memory:")
    init_db(connection)
    yield connection
    connection.close()

@pytest.fixture
def client():
    """Фикстура для создания тестового клиента Flask"""
    users.clear()
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def temp_file():
    """Фикстура для создания временного файла"""
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "test_report.txt")
    yield file_path
    # Очистка после теста
    if os.path.exists(file_path):
        os.remove(file_path)
    os.rmdir(temp_dir)
```

## Часть 3. Практические задания

### tests/integration/test_repository.py
```python
import pytest
from app.repository import add_user, get_user_by_name, get_all_users

pytestmark = pytest.mark.integration

class TestDatabaseIntegration:
    """Интеграционные тесты для базы данных"""
    
    def test_add_and_get_user(self, db_connection):
        """Задание 1: Добавление и получение пользователя"""
        # 1. добавляет пользователя в БД
        test_name = "Иван Петров"
        add_user(db_connection, test_name)
        
        # 2. получает пользователя по имени
        user = get_user_by_name(db_connection, test_name)
        
        # 3. проверяет, что пользователь найден
        assert user is not None, "Пользователь не найден в базе данных"
        
        # 4. проверяет, что имя совпадает
        assert user[1] == test_name, f"Ожидалось имя '{test_name}', получено '{user[1]}'"
    
    def test_get_all_users_multiple(self, db_connection):
        """Задание 2: Добавление нескольких пользователей и получение списка"""
        # 1. добавляет двух пользователей
        users_to_add = ["Анна Смирнова", "Петр Иванов"]
        for name in users_to_add:
            add_user(db_connection, name)
        
        # 2. получает список всех пользователей
        all_users = get_all_users(db_connection)
        
        # 3. проверяет, что в базе две записи
        assert len(all_users) == 2, f"Ожидалось 2 записи, получено {len(all_users)}"
        
        # Дополнительная проверка имен
        actual_names = [user[1] for user in all_users]
        assert set(actual_names) == set(users_to_add), "Имена пользователей не совпадают"
    
    @pytest.mark.parametrize("user_name", [
        "Елена Прекрасная",
        "Добрыня Никитич", 
        "Алеша Попович",
        "Илья Муромец"
    ])
    def test_add_user_parametrized(self, db_connection, user_name):
        """Задание 5: Параметризованный тест для нескольких имён пользователей"""
        # Добавляем пользователя
        add_user(db_connection, user_name)
        
        # Проверяем, что пользователь добавлен
        user = get_user_by_name(db_connection, user_name)
        
        assert user is not None, f"Пользователь '{user_name}' не найден"
        assert user[1] == user_name, f"Имя пользователя не совпадает"
    
    def test_add_duplicate_user(self, db_connection):
        """Дополнительный тест: добавление дубликата пользователя"""
        user_name = "Тестовый Пользователь"
        
        # Добавляем первого пользователя
        add_user(db_connection, user_name)
        
        # Добавляем второго пользователя с таким же именем
        add_user(db_connection, user_name)
        
        # Проверяем, что оба добавлены
        all_users = get_all_users(db_connection)
        users_with_name = [user for user in all_users if user[1] == user_name]
        
        assert len(users_with_name) == 2, "Дубликат пользователя не был добавлен"
```

### tests/integration/test_api.py
```python
import pytest
import json

pytestmark = pytest.mark.integration

class TestAPIIntegration:
    """Интеграционные тесты для API"""
    
    def test_create_and_get_user(self, client):
        """Задание 3: Создание пользователя через API и получение списка"""
        # 1. отправляет POST-запрос на /users
        test_user = {"name": "Мария Иванова", "email": "maria@example.com"}
        
        post_response = client.post("/users", 
                                   json=test_user,
                                   content_type="application/json")
        
        # 2. проверяет статус 201
        assert post_response.status_code == 201, "POST запрос не вернул статус 201"
        assert post_response.json == test_user, "Ответ POST запроса не совпадает с отправленными данными"
        
        # 3. отправляет GET-запрос на /users
        get_response = client.get("/users")
        
        # 4. проверяет статус 200
        assert get_response.status_code == 200, "GET запрос не вернул статус 200"
        
        # 5. проверяет, что созданный пользователь присутствует в ответе
        users_list = get_response.json
        assert len(users_list) == 1, "В списке пользователей должно быть ровно 2 элемента"
        assert test_user in users_list, "Созданный пользователь не найден в списке"
    
    def test_empty_users_list(self, client):
        """Задание 6: Проверка пустого списка пользователей API"""
        # GET-запрос к пустому списку пользователей
        get_response = client.get("/users")
        
        # Проверяем статус 200
        assert get_response.status_code == 200, "GET запрос не вернул статус 200"
        
        # Проверяем, что список пользователей пуст
        users_list = get_response.json
        assert isinstance(users_list, list), "Ответ должен быть списком"
        assert len(users_list) == 0, f"Список пользователей не пуст: {users_list}"
    
    def test_multiple_users_creation(self, client):
        """Задание 7: Проверка нескольких POST-запросов"""
        users_to_create = [
            {"name": "Петр Сидоров", "age": 30},
            {"name": "Ольга Кузнецова", "age": 25},
            {"name": "Михаил Васильев", "age": 35}
        ]
        
        # Создаем нескольких пользователей через POST запросы
        for user in users_to_create:
            post_response = client.post("/users", json=user)
            assert post_response.status_code == 201
        
        # Получаем список всех пользователей
        get_response = client.get("/users")
        assert get_response.status_code == 200
        
        # Проверяем, что все созданные пользователи присутствуют
        users_list = get_response.json
        assert len(users_list) == len(users_to_create), \
            f"Ожидалось {len(users_to_create)} пользователей, получено {len(users_list)}"
        
        for expected_user in users_to_create:
            assert expected_user in users_list, f"Пользователь {expected_user} не найден"
    
    def test_create_user_with_invalid_data(self, client):
        """Дополнительный тест: создание пользователя с некорректными данными"""
        # Отправляем пустой запрос
        response = client.post("/users", json={})
        assert response.status_code == 201, "API должен принимать пустые данные"
        
        # Проверяем, что пустой объект был добавлен
        get_response = client.get("/users")
        assert {} in get_response.json, "Пустой объект не был добавлен"
    
    def test_api_response_structure(self, client):
        """Дополнительный тест: проверка структуры ответа API"""
        test_user = {"name": "Тестовый Пользователь", "role": "admin"}
        
        # Создаем пользователя
        post_response = client.post("/users", json=test_user)
        assert post_response.status_code == 201
        
        # Получаем список пользователей
        get_response = client.get("/users")
        users_list = get_response.json
        
        # Проверяем структуру данных
        assert len(users_list) == 1
        created_user = users_list[0]
        assert "name" in created_user, "В ответе отсутствует поле 'name'"
        assert "role" in created_user, "В ответе отсутствует поле 'role'"
        assert created_user["name"] == test_user["name"]
        assert created_user["role"] == test_user["role"]
```

### tests/integration/test_files.py
```python
import pytest
import os
from app.files import save_report, read_report

pytestmark = pytest.mark.integration

class TestFilesystemIntegration:
    """Интеграционные тесты для файловой системы"""
    
    def test_file_write_read(self, temp_file):
        """Задание 4: Создание, запись и чтение временного файла"""
        # 1. создаёт временный файл
        # 2. записывает в него текст
        test_text = "Это тестовый отчет для интеграционного тестирования"
        save_report(temp_file, test_text)
        
        # 3. читает содержимое
        read_text = read_report(temp_file)
        
        # 4. сравнивает результат с ожидаемым
        assert read_text == test_text, f"Прочитанный текст не совпадает с записанным"
    
    def test_file_creation_verification(self, temp_file):
        """Задание 8: Проверка существования файла"""
        test_text = "Проверка создания файла"
        
        # Проверяем, что файл не существует до записи
        assert not os.path.exists(temp_file), "Файл не должен существовать до записи"
        
        # Записываем данные
        save_report(temp_file, test_text)
        
        # 1. проверяем, что файл был создан
        assert os.path.exists(temp_file), "Файл не был создан"
        
        # 2. проверяем, что файл не пустой
        assert os.path.getsize(temp_file) > 0, "Файл пустой"
        
        # 3. проверяем содержимое
        read_text = read_report(temp_file)
        assert read_text == test_text, "Содержимое файла не совпадает"
    
    def test_multiple_lines_file(self, temp_file):
        """Дополнительный тест: работа с многострочным файлом"""
        test_lines = [
            "Первая строка отчета",
            "Вторая строка отчета",
            "Третья строка отчета"
        ]
        test_text = "\n".join(test_lines)
        
        # Записываем многострочный текст
        save_report(temp_file, test_text)
        
        # Читаем и проверяем
        read_text = read_report(temp_file)
        
        assert read_text == test_text, "Многострочный текст не совпадает"
        assert len(read_text.split("\n")) == len(test_lines), "Количество строк не совпадает"
    
    def test_empty_file(self, temp_file):
        """Дополнительный тест: создание пустого файла"""
        # Записываем пустую строку
        save_report(temp_file, "")
        
        # Проверяем, что файл создан
        assert os.path.exists(temp_file), "Файл не создан"
        
        # Читаем и проверяем
        read_text = read_report(temp_file)
        assert read_text == "", "Файл не пустой"
    
    def test_file_overwrite(self, temp_file):
        """Дополнительный тест: перезапись файла"""
        # Первая запись
        first_text = "Первое содержимое"
        save_report(temp_file, first_text)
        
        # Проверяем первое содержимое
        assert read_report(temp_file) == first_text
        
        # Вторая запись (перезапись)
        second_text = "Второе содержимое"
        save_report(temp_file, second_text)
        
        # Проверяем, что содержимое обновилось
        assert read_report(temp_file) == second_text
        assert read_report(temp_file) != first_text, "Файл не был перезаписан"
```

### tests/__init__.py
```python
# Пустой файл для обозначения пакета
```

### tests/integration/__init__.py
```python
# Пустой файл для обозначения пакета
```

## Команды для запуска тестов

Вот команды для запуска всех созданных тестов:

### 1. Установка зависимостей
```bash
pip install pytest flask
```

### 2. Запуск всех тестов
```bash
pytest
```

### 3. Запуск только интеграционных тестов
```bash
pytest -m integration
```

### 4. Подробный вывод
```bash
pytest -v
```

### 5. Запуск конкретного тестового файла
```bash
pytest tests/integration/test_repository.py -v
pytest tests/integration/test_api.py -v
pytest tests/integration/test_files.py -v
```

### 6. Запуск с отчетом о покрытии (если установлен pytest-cov)
```bash
pip install pytest-cov
pytest --cov=app tests/
```

## Пояснения к тестам

### Отличия интеграционных тестов от unit-тестов:

1. **Интеграционные тесты** проверяют взаимодействие между компонентами:
   - База данных: реальные запросы SQL
   - API: реальные HTTP-запросы
   - Файловая система: реальные операции с файлами

2. **Изоляция с помощью фикстур**:
   - `db_connection`: использует in-memory базу данных
   - `client`: создает тестовый клиент Flask
   - `temp_file`: создает временные файлы

3. **Маркеры**: используются для группировки и выборочного запуска тестов

Эта структура обеспечивает полную изоляцию тестов и позволяет проверить реальное взаимодействие компонентов системы без влияния на основное окружение.
