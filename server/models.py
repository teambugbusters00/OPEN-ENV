"""Data models for OpenEnv trading environment."""
from pydantic import BaseModel
from typing import Optional, Any


class Tbench2State(BaseModel):
    """Current state observation."""
    price: float
    trend: float
    position: Optional[str]


class Tbench2Action(BaseModel):
    """Trading action."""
    action: str  # "buy", "sell", "hold"


class Tbench2Observation(BaseModel):
    """Step observation response."""
    state: Tbench2State
    reward: float
    done: bool
    info: dict[str, Any]
