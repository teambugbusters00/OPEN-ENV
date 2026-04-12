"""Inference script with LiteLLM for decision making."""

import os
import requests
import json
import sys
from openai import OpenAI

SPACE_URL = os.environ.get("SPACE_URL", "http://localhost:7860")
API_BASE_URL = os.environ.get("API_BASE_URL", "")
API_KEY = os.environ.get("API_KEY", "dummy")

client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)


def log_start(task_id="easy"):
    """Log episode start with strict format."""
    print(f"[START] task={task_id} env=openenv model=gpt-4o")


def log_step(step_num, action, reward, done, error=None):
    """Log step with strict format."""
    error_str = "null" if error is None else f'"{error}"'
    print(
        f"[STEP] step={step_num} action={action} reward={reward} done={str(done).lower()} error={error_str}"
    )


def log_end(success, steps, score, rewards):
    """Log episode end with strict format."""
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}"
    )


def get_llm_decision(state, step_num):
    """Get trading decision from LLM."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a trading agent. Current state: {state}. Available actions: buy, sell, hold. Respond with only one word: buy, sell, or hold.",
                },
                {
                    "role": "user",
                    "content": f"What action should I take at step {step_num}?",
                },
            ],
            max_tokens=10,
        )
        decision = response.choices[0].message.content.strip().lower()
        if decision not in ["buy", "sell", "hold"]:
            return "hold"
        return decision
    except Exception as e:
        print(f"[LLM ERROR] {e}", file=sys.stderr)
        return "hold"


def run_episode(task_id="easy"):
    """Run single episode with LLM decision making."""
    try:
        log_start(task_id)

        response = requests.post(f"{SPACE_URL}/reset")
        if response.status_code != 200:
            log_end(False, 0, 0.0, [])
            return False

        state = response.json()

        rewards = []
        step = 0
        max_steps = 9

        while step < max_steps:
            action = get_llm_decision(state, step)

            response = requests.post(f"{SPACE_URL}/step", json={"action": action})

            if response.status_code != 200:
                log_step(step + 1, action, 0.0, True, "API error")
                break

            result = response.json()
            reward = result.get("reward", 0.0)
            done = result.get("done", False)
            state = result
            rewards.append(reward)

            log_step(step + 1, action, reward, done)

            if done:
                break

            step += 1

        total_reward = sum(rewards)
        score = min(total_reward / 2.0, 1.0)

        log_end(True, len(rewards), score, rewards)
        return True

    except Exception as e:
        print(f"[ERROR] {str(e)}", file=sys.stderr)
        log_end(False, 0, 0.0, [])
        return False


def main():
    """Run inference with all tasks."""
    tasks = ["easy", "medium", "hard"]
    results = []

    for task_id in tasks:
        success = run_episode(task_id)
        results.append({"task": task_id, "success": success})
        print()

    print(
        f"[SUMMARY] completed={len(results)} tasks={','.join(t['task'] for t in results)}"
    )

    return all(r["success"] for r in results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
