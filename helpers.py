import random
import string
import allure

@allure.step("Генерация случайной строки")
def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@allure.step("Создание уникальных данных для регистрации пользователя")
def generate_user_payload():
    return {
        "email": f"{generate_random_string()}@yandex.ru",
        "password": generate_random_string(),
        "name": generate_random_string()
    }
