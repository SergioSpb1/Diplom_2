import allure

@allure.suite("Тестирование логина пользователя")
class TestLoginUser:

    @allure.title("Успешная авторизация пользователя с валидными учетными данными")
    def test_authorize_registered_user_with_valid_credentials_returns_tokens(self, user_client, created_user):
        # Берем данные юзера, которого фикстура уже зарегистрировала в базе
        payload = created_user["payload"]
        
        login_payload = {
            "email": payload["email"],
            "password": payload["password"]
        }
        
        # Отправляем запрос на вход
        response = user_client.login_user(login_payload)
        
        # Проверяем успешный статус и наличие токенов в ответе
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    @allure.title("Ошибка авторизации при отправке некорректного пароля")
    def test_authorize_user_with_invalid_password_not_allowed(self, user_client, created_user):
        # Берем почту существующего юзера, но ломаем ему пароль
        payload = created_user["payload"]
        
        login_payload = {
            "email": payload["email"],
            "password": "wrong_password_123"
        }
        
        # Пытаемся войти с плохим паролем
        response = user_client.login_user(login_payload)
        
        # Проверяем ошибку 401 и текст сообщения из документации
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"

    @allure.title("Ошибка авторизации при отправке незарегистрированного email")
    def test_authorize_user_with_invalid_email_not_allowed(self, user_client, created_user):
        # Берем пароль существующего юзера, но отправляем несуществующую почту
        payload = created_user["payload"]
        
        login_payload = {
            "email": "non_existent_user_email_999@yandex.ru",
            "password": payload["password"]
        }
        
        # Пытаемся войти с плохим email
        response = user_client.login_user(login_payload)
        
        # Проверяем ошибку 401 и текст сообщения из документации
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"
