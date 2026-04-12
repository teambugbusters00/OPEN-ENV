"""Easy trading task - simple upward trend."""


class EasyTask:
    """Simple upward trend task.
    
    Prices: [100, 102, 101, 105, 110, 108, 112, 115, 113, 120]
    Strategy: Buy low, sell high on uptrends
    Expected: Identify clear uptrend from 100->110, enter and exit profitably
    """

    def __init__(self):
        """Initialize easy task."""
        self.prices = [100, 102, 101, 105, 110, 108, 112, 115, 113, 120]
        self.description = "Simple upward trend - identify and trade the trend"
        self.difficulty = "easy"

    def get_prices(self):
        """Get price history."""
        return self.prices

    def get_optimal_trades(self):
        """Get optimal trades for this task."""
        # Optimal: buy at 100, sell at 120 = profit 20
        return [(100, 120)]

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
        max_profit = 20.0  # 100 -> 120
        
        score = total_profit / max_profit
        return max(0.0, min(score, 1.0))
