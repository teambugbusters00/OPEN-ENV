"""Grader for hard trading task."""


def grade_hard(trades: list) -> dict:
    """Grade hard trading task.
    
    Args:
        trades: list of rewards from episode
        
    Returns:
        {
            "score": float in [0, 1],
            "feedback": str,
            "max_possible": float
        }
    """
    if not trades:
        return {
            "score": 0.0,
            "feedback": "No trades executed. Required: risk management and reversal detection.",
            "max_possible": 1.0
        }

    total_reward = sum(trades)
    max_reward = 1.5  # max profit of 15 / 10 normalization
    
    # Heavy penalty for losses (negative trades mean we lost money)
    negative_trades = [t for t in trades if t < 0]
    loss_penalty = len(negative_trades) * 0.1
    
    score = min(total_reward / max_reward, 1.0) - loss_penalty
    score = max(0.0, score)
    
    feedback = f"Total reward: {total_reward:.2f}, losses: {len(negative_trades)}. Strategy: risk control."
    
    return {
        "score": round(score, 3),
        "feedback": feedback,
        "max_possible": 1.0
    }
