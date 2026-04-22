from django.contrib import admin
from django.urls import path, include
from accounts.views import RegisterView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API v1 Versioning
    path('api/v1/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/v1/auth/login/', LoginView.as_view(), name='auth_login'),
    
    # Watchlist App URLs
    path('api/v1/', include('watchlist.urls')),
]
