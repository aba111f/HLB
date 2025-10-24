from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import  ExchangeRequestViewSet

router = DefaultRouter() 

router.register(r'exchange-requests', ExchangeRequestViewSet, basename='exchange-request')

urlpatterns = [
    path('', include(router.urls)),
]