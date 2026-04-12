"""Grader for easy trading task."""


def grade_easy(trades: list) -> dict:
    """Grade easy trading task.
    
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
            "feedback": "No profitable trades executed",
            "max_possible": 1.0
        }

    total_reward = sum(trades)
    max_reward = 2.0  # max profit of 20 / 10 normalization
    
    score = min(total_reward / max_reward, 1.0)
    score = max(0.0, score)
    
    feedback = f"Total reward: {total_reward:.2f}. Strategy: simple upward trend recognition."
    
    return {
        "score": round(score, 3),
        "feedback": feedback,
        "max_possible": 1.0
    }
