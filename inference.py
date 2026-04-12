"""Inference script with LiteLLM for decision making."""

import asyncio
import os
import json
import sys
import requests
from openai import OpenAI
from typing import List, Optional

SPACE_URL = os.environ.get("SPACE_URL", "http://localhost:7860")
API_KEY = os.environ.get("API_KEY", "")
API_BASE_URL = os.environ.get("API_BASE_URL", "")

if not API_KEY:
    API_KEY = os.environ.get("HF_TOKEN", "dummy")
if not API_BASE_URL:
    API_BASE_URL = "https://router.huggingface.co/v1"

MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
MAX_STEPS = 8
SUCCESS_SCORE_THRESHOLD = 0.4
TASKS = ["easy", "medium", "hard"]

client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(
    step: int, action: str, reward: float, done: bool, error: Optional[str]
) -> None:
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


def get_model_action(step: int, obs_dict: dict) -> dict:
    """Get trading decision from LLM."""
    try:
        user_prompt = f"Step: {step}\nCurrent State: {json.dumps(obs_dict)}\n\nAvailable actions: buy, sell, hold. Respond with a JSON object with 'action' key only."

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a trading agent. Analyze the current state and respond with a JSON object containing only one key: 'action' with value 'buy', 'sell', or 'hold'.",
                },
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            max_tokens=50,
        )

        text = (completion.choices[0].message.content or "").strip()

        # Parse JSON from response
        try:
            data = json.loads(text)
            action = data.get("action", "hold")
        except:
            # Fallback: extract action from text
            text_lower = text.lower()
            if "buy" in text_lower:
                action = "buy"
            elif "sell" in text_lower:
                action = "sell"
            else:
                action = "hold"

        if action not in ["buy", "sell", "hold"]:
            action = "hold"
        return {"action": action}

    except Exception as e:
        print(f"[LLM ERROR] {e}", file=sys.stderr)
        return {"action": "hold", "error": str(e)}


async def run_episode(task_id: str = "easy"):
    """Run single episode with LLM decision making."""
    try:
        log_start(task=task_id, env="openenv", model=MODEL_NAME)

        response = requests.post(f"{SPACE_URL}/reset", timeout=30)
        if response.status_code != 200:
            log_end(False, 0, 0.001, [])
            return False

        state = response.json()
        obs_dict = state.get("state", {})

        rewards = []
        step = 0
        max_steps = MAX_STEPS
        last_reward = 0.0

        while step < max_steps:
            ai_response = get_model_action(step, obs_dict)
            action = ai_response.get("action", "hold")
            error = ai_response.get("error")

            response = requests.post(
                f"{SPACE_URL}/step", json={"action": action}, timeout=30
            )

            if response.status_code != 200:
                log_step(step + 1, action, 0.001, True, "API error")
                break

            result = response.json()
            reward = result.get("reward", 0.001)
            done = result.get("done", False)
            obs_dict = result.get("state", {})
            rewards.append(reward)
            last_reward = reward

            log_step(
                step=step + 1, action=action, reward=reward, done=done, error=error
            )

            if done:
                break

            step += 1

        total_reward = sum(rewards)
        score = min(total_reward / 2.0, 1.0)
        score = min(max(score, 0.001), 0.999)

        success = score >= SUCCESS_SCORE_THRESHOLD

        log_end(success=success, steps=step + 1, score=score, rewards=rewards)
        return True

    except Exception as e:
        print(f"[ERROR] {str(e)}", file=sys.stderr)
        log_end(False, 0, 0.001, [])
        return False


async def main():
    """Run inference with all tasks."""
    for task_id in TASKS:
        await run_episode(task_id)


if __name__ == "__main__":
    asyncio.run(main())
