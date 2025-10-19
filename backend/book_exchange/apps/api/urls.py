from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, BookViewSet, ExchangeRequestViewSet,CustomLoginView, search_books

router = DefaultRouter()                
router.register(r'users', UserViewSet, basename='user')
router.register(r'books', BookViewSet, basename='book')
router.register(r'exchange-requests', ExchangeRequestViewSet, basename='exchange-request')
router.register(r'login', CustomLoginView, basename='custom-login')

urlpatterns = [
    path('', include(router.urls)),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', search_books)
]

# Подсказочки :)  (крч /help)

# <--!! Пользователи !!-->

# POST /api/users/ → создать пользователя

# GET /api/users/ → список пользователей

# GET /api/users/{id}/ → данные конкретного пользователя

# PUT /api/users/{id}/ → обновить

# DELETE /api/users/{id}/ → удалить

# POST /api/users/search_and_filter/ → фильтр по городам и книгам (в теле массивы cities и books)




# <--!! Книги !!-->

# POST /api/books/ → добавить книгу

# POST /api/search/ -> search kniga

# GET /api/books/ → список всех книг

# GET /api/books/{id}/ → конкретная книга

# PUT /api/books/{id}/ → обновить книгу

# DELETE /api/books/{id}/ → удалить




# <--!! Запросы на обмен !!-->

# POST /api/exchange-requests/ → отправить запрос

# GET /api/exchange-requests/ → список запросов

# GET /api/exchange-requests/{id}/ → запрос детально

# PUT /api/exchange-requests/{id}/ → обновить (например, поменять статус)

# DELETE /api/exchange-requests/{id}/ → удалить