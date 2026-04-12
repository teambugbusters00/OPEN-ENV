"""Hard trading task - fake breakout with risk management."""


class HardTask:
    """Fake breakout detection and risk management.
    
    Prices: [100, 105, 110, 108, 112, 115, 111, 106, 102, 98]
    Strategy: Detect fake breakouts, manage risk on reversals
    Expected: Avoid overtrading, minimize losses on reversals
    """

    def __init__(self):
        """Initialize hard task."""
        self.prices = [100, 105, 110, 108, 112, 115, 111, 106, 102, 98]
        self.description = "Fake breakout - risk control and reversal detection"
        self.difficulty = "hard"

    def get_prices(self):
        """Get price history."""
        return self.prices

    def get_optimal_trades(self):
        """Get optimal trades for this task."""
        # Only catch 100->115 and avoid the reversal = 15
        # Or just one profitable: 100->110 = 10
        return [(100, 115)]

    def evaluate(self, trades):
        """Evaluate trades against task.
        
        Args:
            trades: list of (entry, exit) tuples
            
        Returns:
            score in [0, 1]
        """
        if not trades:
            return 0.0

        total_profit = sum(max(0, exit - entry) for entry, exit in trades)
        total_loss = sum(max(0, entry - exit) for entry, exit in trades)
        
        max_profit = 15.0
        
        # Heavy penalty for losses (risk management is key)
        loss_penalty = total_loss / 10.0
        
        score = (total_profit / max_profit) - loss_penalty
        return max(0.0, min(score, 1.0))
