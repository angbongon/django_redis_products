from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"orders", views.OrderViewSet, basename='orders')
router.register(r"products", views.ProductViewSet, basename='products')

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"auth/", include("rest_auth.urls")),
]
