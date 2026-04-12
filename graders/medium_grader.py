"""Grader for medium trading task."""


def grade_medium(trades: list) -> dict:
    """Grade medium trading task.
    
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
            "feedback": "No trades executed. Required: handle volatility without overtrading.",
            "max_possible": 1.0
        }

    total_reward = sum(trades)
    num_trades = len(trades)
    max_reward = 1.5  # max profit of 15 / 10 normalization
    
    # Penalize excessive trading
    overtrading_penalty = max(0, (num_trades - 2) * 0.05)
    
    score = min(total_reward / max_reward, 1.0) - overtrading_penalty
    score = max(0.0, score)
    
    feedback = f"Total reward: {total_reward:.2f}, trades: {num_trades}. Strategy: volatility management."
    
    return {
        "score": round(score, 3),
        "feedback": feedback,
        "max_possible": 1.0
    }
