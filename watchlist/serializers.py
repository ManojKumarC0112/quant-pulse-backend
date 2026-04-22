from rest_framework import serializers
from .models import WatchlistAsset
from .services.risk_engine import RiskEngine

class WatchlistAssetSerializer(serializers.ModelSerializer):
    risk_analysis = serializers.SerializerMethodField()

    class Meta:
        model = WatchlistAsset
        fields = ['id', 'symbol', 'target_price', 'current_price', 'entry_price', 'notes', 'risk_analysis', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_risk_analysis(self, obj):
        return RiskEngine.evaluate_risk(obj.current_price, obj.target_price)

    def create(self, validated_data):
        # Automatically tie user from request context
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
