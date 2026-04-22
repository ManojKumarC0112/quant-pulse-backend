from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WatchlistViewSet, AdminWatchlistViewSet, health_check

router = DefaultRouter()
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'admin/watchlist', AdminWatchlistViewSet, basename='admin_watchlist')

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('', include(router.urls)),
]
