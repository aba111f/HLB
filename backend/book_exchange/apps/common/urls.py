from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomLoginView, SearchViewSet

router = DefaultRouter()                

router.register(r'login', CustomLoginView, basename='custom-login')
router.register(r'search', SearchViewSet, basename='book-search')

urlpatterns = [
    path('', include(router.urls)),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('search/', search_books)
]

# common/login/ -> login user
