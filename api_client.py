import requests
import allure
from data import Urls

class UserApiClient:
    
    @allure.step("Отправка API-запроса на регистрацию нового пользователя")
    def register_user(self, payload):
        return requests.post(Urls.CREATE_USER, json=payload)
        
    @allure.step("Отправка API-запроса на авторизацию (логин) пользователя")
    def login_user(self, payload):
        return requests.post(Urls.LOGIN_USER, json=payload)
        
    @allure.step("Отправка API-запроса на удаление данных пользователя")
    def delete_user(self, access_token):
        headers = {"Authorization": access_token}
        return requests.delete(Urls.USER_DATA, headers=headers)


class KitchenApiClient:

    @allure.step("Запрос списка доступных ингредиентов с сервера")
    def fetch_available_ingredients(self):
        return requests.get(Urls.INGREDIENTS)

    @allure.step("Отправка API-запроса на формирование нового заказа")
    def dispatch_new_order(self, order_data, authorization_token=None):
        request_headers = {}
        if authorization_token:
            request_headers["Authorization"] = authorization_token
        return requests.post(Urls.ORDERS, json=order_data, headers=request_headers)
