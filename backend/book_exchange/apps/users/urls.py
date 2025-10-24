from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()                
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),  
]

# POST /api/users/ → создать пользователя

# GET /api/users/ → список пользователей

# GET /api/users/{id}/ → данные конкретного пользователя

# PUT /api/users/{id}/ → обновить

# DELETE /api/users/{id}/ → удалить

# POST /api/users/search_and_filter/ → фильтр по городам и книгам (в теле массивы cities и books)