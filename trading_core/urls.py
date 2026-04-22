from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import RegisterView, LoginView

schema_view = get_schema_view(
   openapi.Info(
      title="Trading Pulse API",
      default_version='v1',
      description="Elite Intelligent Watchlist API for Primetrade.ai",
      contact=openapi.Contact(email="contact@tradingpulse.ai"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API v1 Versioning
    path('api/v1/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/v1/auth/login/', LoginView.as_view(), name='auth_login'),
    
    # Watchlist App URLs
    path('api/v1/', include('watchlist.urls')),
]
