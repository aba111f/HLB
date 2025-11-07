from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import  ExchangeRequestViewSet

router = DefaultRouter() 

router.register(r'', ExchangeRequestViewSet, basename='exchange-requests')

urlpatterns = [
    path('', include(router.urls)),
]