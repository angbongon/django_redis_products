from django.urls import path, include

from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from api import views

router = DefaultRouter()
router.register(r"orders", views.OrderViewSet, basename='orders')
router.register(r"products", views.ProductViewSet, basename='products')

schema_view = get_schema_view(
    openapi.Info(
        title="Django Products API",
        default_version='v1',
        description="Django Products API docs",
        contact=openapi.Contact(email="angbonillagonzalez@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[]
)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'auth/', include('rest_auth.urls')),
    # path(r'swagger(?P<format>\.json|\.yaml)',
    #     schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path(r'swagger/', schema_view.with_ui('swagger',
    #     cache_timeout=0), name='schema-swagger-ui'),
    path(r'docs/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
