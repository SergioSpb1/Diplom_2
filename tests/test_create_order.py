import allure

@allure.suite("Тестирование отправки и формирования заказов")
class TestCreateOrder:

    @allure.title("Успешное оформление заказа авторизованным пользователем с ингредиентами")
    def test_submit_order_by_authenticated_client_with_ingredients_success(self, kitchen_client, created_user, available_ingredient_hashes):
        # Покрывает пункты: «с авторизацией» и «с ингредиентами»
        fresh_user_token = created_user["access_token"]
        
        burger_ingredients = {
            "ingredients": [available_ingredient_hashes[0], available_ingredient_hashes[1]]
        }
        
        server_response = kitchen_client.dispatch_new_order(burger_ingredients, authorization_token=fresh_user_token)
        
        assert server_response.status_code == 200
        assert server_response.json().get("success") is True
        assert "order" in server_response.json()

    @allure.title("Успешное оформление заказа неавторизованным пользователем с ингредиентами")
    def test_submit_order_by_anonymous_guest_with_ingredients_success(self, kitchen_client, available_ingredient_hashes):
        # Покрывает пункты: «без авторизации» и «с ингредиентами»
        burger_ingredients = {
            "ingredients": [available_ingredient_hashes[0], available_ingredient_hashes[1]]
        }
        
        server_response = kitchen_client.dispatch_new_order(burger_ingredients)
        
        assert server_response.status_code == 200
        assert server_response.json().get("success") is True
        assert "order" in server_response.json()

    @allure.title("Отказ в оформлении при отправке пустого списка ингредиентов")
    def test_submit_order_without_any_ingredients_not_allowed(self, kitchen_client, created_user):
        fresh_user_token = created_user["access_token"]
        
        burger_ingredients = {
            "ingredients": []
        }
        
        server_response = kitchen_client.dispatch_new_order(burger_ingredients, authorization_token=fresh_user_token)
        
        assert server_response.status_code == 400
        assert server_response.json().get("success") is False
        assert server_response.json().get("message") == "Ingredient ids must be provided"

    @allure.title("Ошибка сервера при создании заказа с неверным хешем ингредиентов")
    def test_submit_order_with_corrupted_ingredient_hash_returns_500(self, kitchen_client, created_user):
        fresh_user_token = created_user["access_token"]
        
        burger_ingredients = {
            "ingredients": ["broken_hash_abc_373"]
        }
        
        server_response = kitchen_client.dispatch_new_order(burger_ingredients, authorization_token=fresh_user_token)
        
        assert server_response.status_code == 500
