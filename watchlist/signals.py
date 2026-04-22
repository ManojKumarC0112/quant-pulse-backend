from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WatchlistAsset, WatchlistAuditLog

@receiver(post_save, sender=WatchlistAsset)
def audit_watchlist_mutations(sender, instance, created, **kwargs):
    """
    Event-driven subscriber tracking changes to the WatchlistAsset.
    Completely decouples auditing logic from the HTTP views.
    """
    action = 'CREATED' if created else 'UPDATED'
    if instance.is_deleted:
        action = 'SOFT_DELETED'
        
    WatchlistAuditLog.objects.create(
        asset=instance,
        action=action,
        new_price=instance.current_price
    )
