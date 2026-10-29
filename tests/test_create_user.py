import pytest
import allure
from helpers import generate_user_payload

@allure.suite("Тестирование создания пользователя")
class TestCreateUser:

    @pytest.fixture(autouse=True)
    def setup_garbage_collection(self, user_client):
        self.tokens_to_delete = []
        yield
        for token in self.tokens_to_delete:
            if token:
                user_client.delete_user(token)

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_client):
        payload = generate_user_payload()
        response = user_client.register_user(payload)
        
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "accessToken" in response.json()
        
        self.tokens_to_delete.append(response.json().get("accessToken"))

    @allure.title("Ошибка при создании уже зарегистрированного пользователя")
    def test_create_duplicate_user_not_allowed(self, user_client):
        payload = generate_user_payload()
        
        first_response = user_client.register_user(payload)
        self.tokens_to_delete.append(first_response.json().get("accessToken"))
        
        duplicate_response = user_client.register_user(payload)
        
        assert duplicate_response.status_code == 403
        assert duplicate_response.json().get("success") is False
        assert duplicate_response.json().get("message") == "User already exists"


    @allure.title("Ошибка при создании пользователя с незаполненным обязательным полем")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_not_allowed(self, user_client, missing_field):
        payload = generate_user_payload()
        payload[missing_field] = ""
        
        response = user_client.register_user(payload)
        
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == "Email, password and name are required fields"