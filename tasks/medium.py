"""Medium trading task - volatile market with multiple opportunities."""


class MediumTask:
    """Volatile market with multiple trading opportunities.
    
    Prices: [100, 98, 102, 99, 105, 103, 108, 101, 110, 107]
    Strategy: Handle volatility, identify real trends vs noise
    Expected: Capture uptrends while avoiding overtrading
    """

    def __init__(self):
        """Initialize medium task."""
        self.prices = [100, 98, 102, 99, 105, 103, 108, 101, 110, 107]
        self.description = "Volatile market - avoid overtrading, capture real trends"
        self.difficulty = "medium"

    def get_prices(self):
        """Get price history."""
        return self.prices

    def get_optimal_trades(self):
        """Get optimal trades for this task."""
        # Strategy: (99->105) and (101->110) = 6 + 9 = 15
        return [(99, 105), (101, 110)]

    def evaluate(self, trades):
        """Evaluate trades against task.
        
        Args:
            trades: list of (entry, exit) tuples
            
        Returns:
            score in [0, 1]
        """
        if not trades:
            return 0.0

        total_profit = sum(exit - entry for entry, exit in trades)
        max_profit = 15.0
        
        # Penalize overtrading (more than 3 trades)
        trade_penalty = max(0, (len(trades) - 3) * 0.05)
        
        score = (total_profit / max_profit) - trade_penalty
        return max(0.0, min(score, 1.0))
