"""FastAPI application for OpenEnv trading environment."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from server.env import TradingEnv
from server.models import Tbench2Action, Tbench2Observation

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create app and environment
app = FastAPI(
    title="Trading Environment",
    description="OpenEnv trading environment API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
env = TradingEnv()


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "environment": "trading_env"}


@app.post("/reset")
def reset():
    """Reset environment to initial state.
    
    Returns:
        {
            "state": {
                "price": float,
                "trend": float,
                "position": str or null
            },
            "info": {
                "error": str or null
            }
        }
    """
    try:
        result = env.reset()
        logger.info(f"Environment reset: {result}")
        return result
    except Exception as e:
        logger.error(f"Reset error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/step")
def step(action: Tbench2Action):
    """Execute one step in environment.
    
    Args:
        action: Tbench2Action with action field ("buy", "sell", "hold")
        
    Returns:
        {
            "state": {...},
            "reward": float in [0, 1],
            "done": bool,
            "info": {"error": str or null}
        }
    """
    try:
        act = action.action.lower()
        if act not in ["buy", "sell", "hold"]:
            return {
                "state": env._get_state(),
                "reward": 0.0,
                "done": False,
                "info": {"error": f"Invalid action: {act}"}
            }
        
        result = env.step(act)
        logger.info(f"Step executed: action={act}, reward={result['reward']}, done={result['done']}")
        return result
    except Exception as e:
        logger.error(f"Step error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/close")
def close():
    """Close environment."""
    try:
        result = env.close()
        logger.info("Environment closed")
        return result
    except Exception as e:
        logger.error(f"Close error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """Main entry point for the trading environment server."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)


if __name__ == "__main__":
    main()
