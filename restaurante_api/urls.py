from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurante.views import PratoViewSet, PedidoViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Configuração do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Restaurante",
        default_version='v1',
        description="Documentação da API do Sistema de Restaurante",
        terms_of_service="https://www.seusite.com/terms/",
        contact=openapi.Contact(email="contato@seusite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Roteador da API
router = DefaultRouter()
router.register(r'v1/pratos', PratoViewSet, basename='pratos')
router.register(r'v1/pedidos', PedidoViewSet, basename='pedidos')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include(router.urls)),
    
    # Autenticação
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Documentação
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]