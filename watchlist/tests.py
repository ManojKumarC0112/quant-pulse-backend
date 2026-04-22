from django.test import TestCase
from decimal import Decimal
from .services.risk_engine import RiskEngine

class RiskEnginePrioritizationTest(TestCase):
    def test_high_risk_trigger(self):
        """Test that a gap <= 2% results in HIGH risk."""
        # Target 100, current 99 = 1% gap
        result = RiskEngine.evaluate_risk(Decimal('99.00'), Decimal('100.00'))
        self.assertEqual(result['risk_level'], 'HIGH')
        self.assertTrue(result['risk_score'] <= 0.02)

    def test_medium_risk_trigger(self):
        """Test that a gap <= 5% results in MEDIUM risk."""
        # Target 100, current 96 = 4% gap
        result = RiskEngine.evaluate_risk(Decimal('96.00'), Decimal('100.00'))
        self.assertEqual(result['risk_level'], 'MEDIUM')

    def test_low_risk_trigger(self):
        """Test that a gap > 5% results in LOW risk."""
        # Target 100, current 90 = 10% gap
        result = RiskEngine.evaluate_risk(Decimal('90.00'), Decimal('100.00'))
        self.assertEqual(result['risk_level'], 'LOW')
        
    def test_zero_division_guard(self):
        """Test edge cases to prevent unhandled exceptions on invalid assets."""
        result = RiskEngine.evaluate_risk(Decimal('0'), Decimal('100.00'))
        self.assertEqual(result['risk_level'], 'UNKNOWN')
