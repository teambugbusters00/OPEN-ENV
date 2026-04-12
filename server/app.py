"""FastAPI application for OpenEnv trading environment."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from server.env import TradingEnv
from server.models import Tbench2Action, Tbench2Observation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Trading Environment",
    description="OpenEnv trading environment API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = TradingEnv()


@app.get("/")
def root():
    return {"status": "ok", "environment": "trading_env"}


@app.post("/reset")
async def reset():
    try:
        result = env.reset()
        logger.info(f"Environment reset: {result}")
        return result
    except Exception as e:
        logger.error(f"Reset error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/step")
async def step(action: Tbench2Action):
    try:
        act = action.action.lower()
        if act not in ["buy", "sell", "hold"]:
            return {
                "state": env._get_state(),
                "reward": 0.001,
                "done": False,
                "info": {"error": f"Invalid action: {act}"},
            }

        result = env.step(act)
        logger.info(
            f"Step executed: action={act}, reward={result['reward']}, done={result['done']}"
        )
        return result
    except Exception as e:
        logger.error(f"Step error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/close")
async def close():
    try:
        result = env.close()
        logger.info("Environment closed")
        return result
    except Exception as e:
        logger.error(f"Close error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/score")
async def score():
    try:
        result = env.get_score()
        return {"score": result}
    except Exception as e:
        logger.error(f"Score error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)


if __name__ == "__main__":
    main()
