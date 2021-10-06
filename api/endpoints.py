from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"orders", views.OrderViewSet, basename='orders')
router.register(r"products", views.ProductViewSet, basename='products')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'auth/', include('rest_auth.urls')),
    path(r'api_schema', get_schema_view(title='Django Products API',
         description='An API', version='1.0.0'), name='api_schema'),
    path(r'docs/', TemplateView.as_view(template_name='docs.html',
         extra_context={'schema_url': 'api_schema'}), name='docs')
]
