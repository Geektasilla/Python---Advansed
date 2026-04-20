import json
from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator
from typing import Optional

# Модели:
# Address: Должен содержать следующие поля:
# city: строка, минимум 2 символа.
# street: строка, минимум 3 символа.
# house_number: число, должно быть положительным.

class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)

# User: Должен содержать следующие поля:
# name: строка, должна быть только из букв, минимум 2 символа.
# age: число, должно быть между 0 и 120.
# email: строка, должна соответствовать формату email.
# is_employed: булево значение, статус занятости пользователя.
# address: вложенная модель адреса.
class User(BaseModel):
    name: str = Field(min_length=2, pattern=r"^[a-zA-Z\s]+$")
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

# Валидация:
# Проверка, что если пользователь указывает, что он занят (is_employed = true),
# его возраст должен быть от 18 до 65 лет.
    @model_validator(mode='after')
    def validate_age_employment(self):
        if self.is_employed:
            if not (18 <= self.age <= 65):
                raise ValueError('If employed, age must be between 18 and 65.')
        return self

# Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic,
# валидирует данные, и в случае успеха сериализует объект обратно в JSON и возвращает его.
def process_user_registration(json_input_string: str) -> Optional[str]:
    try:
        user_data = json.loads(json_input_string)
        user = User(**user_data)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None

# Написать несколько примеров JSON строк для проверки различных сценариев валидации:
# успешные регистрации и случаи, когда валидация не проходит (например возраст не соответствует статусу занятости).

print("--- Test Case 1: Successful Registration ---")
json_input_success = """{
    "name": "Jane Doe",
    "age": 30,
    "email": "jane.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Los Angeles",
        "street": "Sunset Blvd",
        "house_number": 456
    }
}"""
processed_user = process_user_registration(json_input_success)
if processed_user:
    print("Successfully registered user:")
    print(processed_user)
print("\n")

print("--- Test Case 2: Successful Registration (Not Employed) ---")
json_input_not_employed = """{
    "name": "Peter Pan",
    "age": 10,
    "email": "peter.pan@neverland.com",
    "is_employed": false,
    "address": {
        "city": "Neverland",
        "street": "Second Star",
        "house_number": 1
    }
}"""
processed_user = process_user_registration(json_input_not_employed)
if processed_user:
    print("Successfully registered user:")
    print(processed_user)
print("\n")

print("--- Test Case 3: Validation Error (Age and Employment Mismatch) ---")
json_input_age_employment_mismatch = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""
processed_user = process_user_registration(json_input_age_employment_mismatch)
if processed_user:
    print("Successfully registered user:")
    print(processed_user)
else:
    print("Validation failed as expected for age and employment mismatch.")
print("\n")

print("--- Test Case 4: Validation Error (Invalid Email) ---")
json_input_invalid_email = """{
    "name": "Alice Wonderland",
    "age": 25,
    "email": "alice@invalid",
    "is_employed": true,
    "address": {
        "city": "Wonderland",
        "street": "Rabbit Hole",
        "house_number": 7
    }
}"""
processed_user = process_user_registration(json_input_invalid_email)
if processed_user:
    print("Successfully registered user:")
    print(processed_user)
else:
    print("Validation failed as expected for invalid email.")
print("\n")

print("--- Test Case 5: Validation Error (Invalid House Number) ---")
json_input_invalid_house_number = """{
    "name": "Bob Builder",
    "age": 40,
    "email": "bob@builder.com",
    "is_employed": true,
    "address": {
        "city": "Construction City",
        "street": "Main Street",
        "house_number": -5
    }
}"""
processed_user = process_user_registration(json_input_invalid_house_number)
if processed_user:
    print("Successfully registered user:")
    print(processed_user)
else:
    print("Validation failed as expected for invalid house number.")
print("\n")

print("--- Test Case 6: Validation Error (Name with numbers) ---")
json_input_name_with_numbers = """{
    "name": "Robot 9000",
    "age": 50,
    "email": "robot@example.com",
    "is_employed": true,
    "address": {
        "city": "Future City",
        "street": "Cyber Avenue",
        "house_number": 100
    }
}"""
processed_user = process_user_registration(json_input_name_with_numbers)
if processed_user:
    print("Successfully registered user:")
    print(processed_user)
else:
    print("Validation failed as expected for name with numbers.")
print("\n")

print("--- Test Case 7: JSON Decode Error (Malformed JSON) ---")
json_input_malformed = """{
    "name": "Malformed Json",
    "age": 30,
    "email": "malformed@example.com",
    "is_employed": true,
    "address": {
        "city": "Error City",
        "street": "Broken Street",
        "house_number": 1
    },
""" # Missing closing brace
processed_user = process_user_registration(json_input_malformed)
if processed_user:
    print("Successfully registered user:")
    print(processed_user)
else:
    print("JSON decode failed as expected for malformed JSON.")
print("\n")
