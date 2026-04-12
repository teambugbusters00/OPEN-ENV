"""Trading environment for OpenEnv."""


class TradingEnv:
    """Simulated trading environment with price history."""

    def __init__(self):
        """Initialize trading environment with price series."""
        self.prices = [100, 102, 101, 105, 110, 108, 112, 115, 113, 120]
        self.reset()

    def reset(self):
        """Reset environment to initial state."""
        self.idx = 1
        self.position = None
        self.entry = 0
        self.trades = []

        return {
            "state": self._get_state(),
            "info": {"error": None}
        }

    def _get_state(self):
        """Get current market state."""
        return {
            "price": self.prices[self.idx],
            "trend": self.prices[self.idx] - self.prices[self.idx - 1],
            "position": self.position
        }

    def step(self, action: str):
        """Execute trading action and step environment.
        
        Args:
            action: Trading action - "buy", "sell", or "hold"
            
        Returns:
            dict with state, reward, done, info
        """
        price = self.prices[self.idx]
        reward = 0.0
        done = False

        if action == "buy" and self.position is None:
            self.position = "long"
            self.entry = price

        elif action == "sell" and self.position == "long":
            profit = price - self.entry
            reward = profit / 10.0  # normalize
            self.trades.append(profit)
            self.position = None

        self.idx += 1

        if self.idx >= len(self.prices):
            done = True

        # Clamp reward to [0, 1]
        reward = max(0.0, min(reward, 1.0))

        return {
            "state": self._get_state(),
            "reward": round(reward, 2),
            "done": done,
            "info": {"error": None}
        }

    def close(self):
        """Close environment."""
        return {"status": "closed"}

    def get_score(self):
        """Calculate normalized score from trades."""
        if not self.trades:
            return 0.0
        
        total_profit = sum(self.trades)
        max_profit = 20.0  # max possible
        
        score = total_profit / max_profit
        return max(0.0, min(score, 1.0))
