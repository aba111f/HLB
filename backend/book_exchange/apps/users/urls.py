from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()                
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),  
]

# POST /users/users/ → создать пользователя

# GET /users/users/ → список пользователей

# GET /users/users/{id}/ → данные конкретного пользователя

# PUT /users/users/{id}/ → обновить

# DELETE /users/users/{id}/ → удалить

# POST /users/users/search_and_filter/ → фильтр по городам и книгам (в теле массивы cities и books)