from decimal import Decimal

class RiskEngine:
    @staticmethod
    def evaluate_risk(current_price: Decimal, target_price: Decimal):
        """
        Intelligently evaluates risk based on price volatility gap.
        Returns a dictionary with 'risk_level', 'risk_score', and 'insight'.
        """
        if current_price <= 0 or target_price <= 0:
            return {
                "risk_level": "UNKNOWN",
                "risk_score": 0.0,
                "insight": "Invalid price data."
            }
            
        # Calculate gap percentage
        gap = abs(target_price - current_price) / current_price
        risk_score = round(float(gap), 4)

        if gap <= Decimal('0.02'):
            return {
                "risk_level": "HIGH",
                "risk_score": risk_score,
                "insight": "High probability trigger; current price is within 2% of target."
            }
        elif gap <= Decimal('0.05'):
            return {
                "risk_level": "MEDIUM",
                "risk_score": risk_score,
                "insight": "Moderate condition; current price is moving within the 5% window."
            }
        else:
            return {
                "risk_level": "LOW",
                "risk_score": risk_score,
                "insight": "Stable trend; significant price movement still required."
            }
