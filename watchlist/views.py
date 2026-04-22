from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db import connection
from django.db.utils import OperationalError
from accounts.permissions import IsOwnerOrAdmin, IsAdminUser
from .models import WatchlistAsset, WatchlistAuditLog
from .serializers import WatchlistAssetSerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """
    Elite backend microservice health topology check.
    Verifies DB and Cache connections dynamically.
    """
    health = {"status": "ok", "database": "unknown", "cache": "unknown"}
    
    # 1. DB Check
    try:
        connection.ensure_connection()
        health["database"] = "connected"
    except OperationalError:
        health["status"] = "degraded"
        health["database"] = "disconnected"
        
    # 2. Cache Check
    try:
        cache.set("health_ping", "pong", timeout=1)
        if cache.get("health_ping") == "pong":
            health["cache"] = "connected"
        else:
            health["cache"] = "unresponsive"
            health["status"] = "degraded"
    except Exception:
        health["status"] = "degraded"
        health["cache"] = "disconnected"
        
    status_code = status.HTTP_200_OK if health["status"] == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE
    return Response(health, status=status_code)

class WatchlistViewSet(viewsets.ModelViewSet):
    """
    Standard CRUD API for the User's Watchlist.
    """
    serializer_class = WatchlistAssetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['symbol']
    search_fields = ['symbol', 'notes']

    def get_queryset(self):
        # Users only see their own active assets. Admins see nothing here (Admin endpoint is separate).
        if getattr(self, 'swagger_fake_view', False):
            return WatchlistAsset.objects.none()
        return WatchlistAsset.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        # Invalidate the list cache
        cursor = self.request.resolver_match.view_name
        cache.clear() # In a real prod environment we'd use keys to clear appropriately
        serializer.save()
        
    def perform_update(self, serializer):
        cache.clear()
        serializer.save()

    def perform_destroy(self, instance):
        cache.clear()
        instance.delete() # Triggers the soft-delete overriding in the model

    @method_decorator(cache_page(60 * 15)) # 15 minutes cache
    def list(self, request, *args, **kwargs):
        """
        Cached List view for the watchlist to reduce DB IOPS during frequent loads.
        """
        return super().list(request, *args, **kwargs)

class AdminWatchlistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin-only endpoint to view all system-wide active watchlists.
    """
    serializer_class = WatchlistAssetSerializer
    permission_classes = [IsAdminUser]
    queryset = WatchlistAsset.objects.filter(is_deleted=False).select_related('user')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['symbol', 'user__username']
    search_fields = ['symbol', 'user__username', 'notes']
