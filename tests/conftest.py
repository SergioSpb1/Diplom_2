import pytest
import allure
from helpers import generate_user_payload
from api_client import UserApiClient, KitchenApiClient

@pytest.fixture
def user_client():
    return UserApiClient()

@pytest.fixture
def kitchen_client():
    return KitchenApiClient()

@pytest.fixture
def created_user(user_client):
    with allure.step("Фикстура: Автоматическое создание тестового пользователя перед началом теста"):
        payload = generate_user_payload()
        response = user_client.register_user(payload)
        
        user_data = {
            "payload": payload,
            "response_json": response.json(),
            "status_code": response.status_code,
            "access_token": response.json().get("accessToken") if response.status_code == 200 else None
        }
        
    yield user_data
    
    if user_data["access_token"]:
        with allure.step("Фикстура: Удаление тестового пользователя после завершения теста"):
            user_client.delete_user(user_data["access_token"])

@pytest.fixture
def available_ingredient_hashes(kitchen_client):
    with allure.step("Фикстура: Динамическое получение актуальных хешей ингредиентов для формирования заказа"):
        server_response = kitchen_client.fetch_available_ingredients()
        raw_ingredients = server_response.json().get("data", [])
        return [item["_id"] for item in raw_ingredients]

