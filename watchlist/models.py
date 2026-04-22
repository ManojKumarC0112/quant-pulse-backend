from django.db import models
from django.conf import settings

class WatchlistAsset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist')
    symbol = models.CharField(max_length=20)
    target_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    entry_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'symbol']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(current_price__gt=0), name='current_price_gt_zero'),
            models.CheckConstraint(check=models.Q(target_price__gt=0), name='target_price_gt_zero')
        ]
        
    def delete(self, *args, **kwargs):
        """Soft delete the asset"""
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"{self.symbol} - {self.user.username}"


class WatchlistAuditLog(models.Model):
    """
    Immutable ledger tracking modifications to any asset.
    Demonstrates event-driven architecture and compliance standards.
    """
    asset = models.ForeignKey(WatchlistAsset, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50) # e.g. CREATED, UPDATED, DELETED
    previous_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    new_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.action} on Asset {self.asset_id} at {self.timestamp}"
