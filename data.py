class Urls:
    BASE_URL = "https://stellarburgers.education-services.ru"
    
    # Эндпоинты для работы с пользователем
    CREATE_USER = f"{BASE_URL}/api/auth/register"
    LOGIN_USER = f"{BASE_URL}/api/auth/login"
    USER_DATA = f"{BASE_URL}/api/auth/user"
    
    # Эндпоинты для работы с заказами
    ORDERS = f"{BASE_URL}/api/orders"
    INGREDIENTS = f"{BASE_URL}/api/ingredients"